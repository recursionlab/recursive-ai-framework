"""
Abstract base class for all extractors.
Handles file I/O, checkpointing, parallel processing.
"""

import json
import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
import anthropic
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


@dataclass
class ExtractionResult:
    """Standard result format for all extractors"""
    source_file: str
    source_hash: str
    timestamp: str
    data: Dict[str, Any]
    extraction_type: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = None


class ExtractorBase(ABC):
    """Base class for all extraction scripts"""

    def __init__(
        self,
        repo_path: Path,
        output_dir: Path,
        claude_client: anthropic.Anthropic,
        checkpoint_every: int = 10,
        max_workers: int = 4
    ):
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.claude = claude_client
        self.checkpoint_every = checkpoint_every
        self.max_workers = max_workers

        # Checkpointing
        self.checkpoint_file = self.output_dir / f"{self.extractor_name()}_checkpoint.json"
        self.processed_hashes = self._load_checkpoint()

    @abstractmethod
    def extractor_name(self) -> str:
        """Return the name of this extractor (e.g., 'operator')"""
        pass

    @abstractmethod
    def extract_from_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """
        Extract data from file content.
        Returns list of extracted items.
        """
        pass

    @abstractmethod
    def prompt_template(self) -> str:
        """
        Return the Claude prompt template for this extraction type.
        Can use {content} and {file_path} placeholders.
        """
        pass

    def _file_hash(self, file_path: Path) -> str:
        """Generate hash of file content for deduplication"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return hashlib.sha256(content.encode()).hexdigest()

    def _load_checkpoint(self) -> set:
        """Load set of already-processed file hashes"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_hashes', []))
        return set()

    def _save_checkpoint(self):
        """Save checkpoint of processed files"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({
                'processed_hashes': list(self.processed_hashes),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)

    def find_files(self, pattern: str = "*.md") -> List[Path]:
        """Find all matching files in repo"""
        return list(self.repo_path.rglob(pattern))

    def should_process(self, file_path: Path) -> bool:
        """Check if file needs processing"""
        file_hash = self._file_hash(file_path)
        return file_hash not in self.processed_hashes

    def process_file(self, file_path: Path) -> Optional[ExtractionResult]:
        """Process a single file"""
        try:
            file_hash = self._file_hash(file_path)

            # Skip if already processed
            if file_hash in self.processed_hashes:
                return None

            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Extract using subclass implementation
            extracted_items = self.extract_from_content(content, file_path)

            # Create result
            result = ExtractionResult(
                source_file=str(file_path.relative_to(self.repo_path)),
                source_hash=file_hash,
                timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                data={'items': extracted_items, 'count': len(extracted_items)},
                extraction_type=self.extractor_name()
            )

            # Mark as processed
            self.processed_hashes.add(file_hash)

            return result

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

    def process_all(self, pattern: str = "*.md") -> List[ExtractionResult]:
        """Process all files in parallel"""
        files = self.find_files(pattern)
        files_to_process = [f for f in files if self.should_process(f)]

        print(f"\n{'='*60}")
        print(f"EXTRACTOR: {self.extractor_name().upper()}")
        print(f"{'='*60}")
        print(f"Total files found: {len(files)}")
        print(f"Already processed: {len(files) - len(files_to_process)}")
        print(f"To process: {len(files_to_process)}")
        print(f"{'='*60}\n")

        results = []
        processed_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.process_file, f): f
                for f in files_to_process
            }

            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    processed_count += 1

                    # Progress
                    if processed_count % 10 == 0:
                        print(f"Processed {processed_count}/{len(files_to_process)} files...")

                    # Checkpoint
                    if processed_count % self.checkpoint_every == 0:
                        self._save_checkpoint()
                        self._save_results(results)

        # Final save
        self._save_checkpoint()
        self._save_results(results)

        print(f"\n✓ Extraction complete: {len(results)} results")
        return results

    def _save_results(self, results: List[ExtractionResult]):
        """Save results to JSON"""
        output_file = self.output_dir / f"{self.extractor_name()}s.json"

        # Convert to dict
        data = {
            'metadata': {
                'repo_path': str(self.repo_path),
                'total_files_processed': len(results),
                'extraction_type': self.extractor_name(),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'results': [asdict(r) for r in results]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Saved to: {output_file}")

    def ask_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        """Query Claude with rate limiting"""
        try:
            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Claude API error: {e}")
            return ""
