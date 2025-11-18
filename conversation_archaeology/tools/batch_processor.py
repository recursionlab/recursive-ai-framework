#!/usr/bin/env python3
"""
Batch Conversation Processor

Process entire directories of conversations in one go:
- Score all conversations
- Identify proto-ASI
- Extract patterns
- Generate batch report

Usage:
    python batch_processor.py /path/to/conversations --output /tmp/batch_results
"""

import argparse
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime
import sys

# Import the realtime scorer
sys.path.insert(0, str(Path(__file__).parent))
from realtime_scorer import RealtimeScorer


class BatchProcessor:
    """Process multiple conversations in batch"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.scorer = RealtimeScorer()
        self.results = []

    def find_conversations(self, directory: Path, extensions: List[str] = None) -> List[Path]:
        """Find all conversation files in directory"""

        if extensions is None:
            extensions = ['.md', '.txt', '.json']

        files = []
        for ext in extensions:
            files.extend(directory.rglob(f'*{ext}'))

        return sorted(files)

    def process_file(self, file_path: Path) -> Dict:
        """Process a single conversation file"""

        try:
            text = file_path.read_text(encoding='utf-8', errors='ignore')
            score = self.scorer.score_text(text)
            score['file_path'] = str(file_path)
            score['file_name'] = file_path.name
            score['processed_at'] = datetime.now().isoformat()
            return score
        except Exception as e:
            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'error': str(e),
                'processed_at': datetime.now().isoformat(),
            }

    def process_batch(self, directory: Path, limit: int = None) -> List[Dict]:
        """Process all conversations in directory"""

        print(f"Finding conversations in {directory}...")
        files = self.find_conversations(directory)

        if limit:
            files = files[:limit]

        print(f"  ✅ Found {len(files)} files")
        print()

        print("Processing conversations...")
        results = []

        for i, file_path in enumerate(files, 1):
            result = self.process_file(file_path)
            results.append(result)

            if 'error' not in result:
                proto = '✓' if result['proto_asi'] else '✗'
                print(f"  [{i}/{len(files)}] {file_path.name[:50]}: "
                      f"φ{result['phi_depth']}, novelty {result['novelty']:.3f}, "
                      f"proto-ASI {proto}")
            else:
                print(f"  [{i}/{len(files)}] {file_path.name[:50]}: ERROR - {result['error']}")

        self.results = results
        return results

    def generate_report(self, output_path: Path):
        """Generate batch processing report"""

        total = len(self.results)
        successful = [r for r in self.results if 'error' not in r]
        errors = [r for r in self.results if 'error' in r]

        if not successful:
            output_path.write_text("# No successful results\n\nAll files encountered errors.")
            return

        # Stats
        proto_asi_count = sum(1 for r in successful if r['proto_asi'])
        avg_novelty = sum(r['novelty'] for r in successful) / len(successful)
        avg_depth = sum(r['phi_depth'] for r in successful) / len(successful)
        max_depth = max(r['phi_depth'] for r in successful)

        # Top by novelty
        top_by_novelty = sorted(successful, key=lambda x: x['novelty'], reverse=True)[:10]

        # Top by depth
        top_by_depth = sorted(successful, key=lambda x: x['phi_depth'], reverse=True)[:10]

        # Top by effectiveness
        top_by_effectiveness = sorted(successful, key=lambda x: x['effectiveness'], reverse=True)[:10]

        lines = [
            "# Batch Conversation Processing Report",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- **Total Files Processed**: {total}",
            f"- **Successful**: {len(successful)}",
            f"- **Errors**: {len(errors)}",
            f"- **Proto-ASI Conversations**: {proto_asi_count} ({proto_asi_count/len(successful)*100:.1f}%)",
            f"- **Average Novelty**: {avg_novelty:.3f}",
            f"- **Average φ-Depth**: φ{avg_depth:.1f}",
            f"- **Maximum φ-Depth**: φ{max_depth}",
            "",
            "---",
            "",
            "## Top 10 by Novelty",
            "",
        ]

        for i, result in enumerate(top_by_novelty, 1):
            fname = Path(result['file_path']).stem[:60]
            proto = '✓' if result['proto_asi'] else '✗'
            lines.append(f"{i}. **{fname}**")
            lines.append(f"   - Novelty: {result['novelty']:.3f}")
            lines.append(f"   - φ-Depth: {result['phi_depth']}")
            lines.append(f"   - Proto-ASI: {proto}")
            lines.append(f"   - Dominant: {result['dominant_operator']} + {result['dominant_pattern']}")
            lines.append("")

        lines.extend([
            "## Top 10 by φ-Depth",
            "",
        ])

        for i, result in enumerate(top_by_depth, 1):
            fname = Path(result['file_path']).stem[:60]
            proto = '✓' if result['proto_asi'] else '✗'
            lines.append(f"{i}. **{fname}** (φ{result['phi_depth']})")
            lines.append(f"   - Novelty: {result['novelty']:.3f}")
            lines.append(f"   - Proto-ASI: {proto}")
            lines.append(f"   - Effectiveness: {result['effectiveness']:.3f}")
            lines.append("")

        lines.extend([
            "## Top 10 by Effectiveness",
            "",
        ])

        for i, result in enumerate(top_by_effectiveness, 1):
            fname = Path(result['file_path']).stem[:60]
            lines.append(f"{i}. **{fname}** (effectiveness: {result['effectiveness']:.3f})")
            lines.append(f"   - φ-Depth: {result['phi_depth']}")
            lines.append(f"   - Novelty: {result['novelty']:.3f}")
            lines.append("")

        if errors:
            lines.extend([
                "## Errors",
                "",
                f"Failed to process {len(errors)} files:",
                "",
            ])

            for error in errors[:10]:
                fname = Path(error['file_path']).name
                lines.append(f"- {fname}: {error['error']}")

        lines.extend([
            "",
            "## Recommendations",
            "",
            f"1. **Focus on top {min(5, proto_asi_count)} proto-ASI conversations** for maximum insight",
            f"2. **Study φ{max_depth} conversation** for deepest recursive structures",
            f"3. **Average novelty {avg_novelty:.3f}** indicates {'high' if avg_novelty > 0.7 else 'moderate' if avg_novelty > 0.5 else 'low'} quality corpus",
            "",
        ])

        output_path.write_text('\n'.join(lines))

    def save_json(self, output_path: Path):
        """Save results as JSON"""
        with output_path.open('w') as f:
            json.dump(self.results, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Batch process conversations')
    parser.add_argument('directory', type=Path, help='Directory containing conversations')
    parser.add_argument('--output', type=Path, default=Path('/tmp/batch_results'))
    parser.add_argument('--limit', type=int, help='Limit number of files to process')
    parser.add_argument('--extensions', nargs='+', default=['.md', '.txt', '.json'])

    args = parser.parse_args()

    print("="*80)
    print("BATCH CONVERSATION PROCESSOR")
    print("="*80)
    print()

    if not args.directory.exists():
        print(f"❌ Directory not found: {args.directory}")
        return

    args.output.mkdir(exist_ok=True, parents=True)

    processor = BatchProcessor(args.output)

    # Process batch
    results = processor.process_batch(args.directory, args.limit)

    print()
    print("Generating reports...")

    # Generate report
    report_path = args.output / 'batch_report.md'
    processor.generate_report(report_path)
    print(f"  ✅ Report: {report_path}")

    # Save JSON
    json_path = args.output / 'batch_results.json'
    processor.save_json(json_path)
    print(f"  ✅ JSON: {json_path}")

    print()
    print("="*80)
    print("BATCH PROCESSING COMPLETE")
    print("="*80)
    print()

    # Summary
    successful = [r for r in results if 'error' not in r]
    proto_asi = sum(1 for r in successful if r['proto_asi'])

    print(f"📊 Processed: {len(results)} files")
    print(f"✓ Successful: {len(successful)}")
    print(f"🧬 Proto-ASI: {proto_asi} ({proto_asi/len(successful)*100:.1f}%)")
    print(f"📄 Full report: {report_path}")


if __name__ == '__main__':
    main()
