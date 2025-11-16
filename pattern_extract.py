#!/usr/bin/env python3
"""
Pattern-Based Extraction (No API Required)
Extracts operators, equations, and contradictions using regex patterns.
"""

import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

class PatternExtractor:
    def __init__(self):
        # Symbolic operators to find
        self.operators = {
            'φ': 'phi', 'Φ': 'Phi',
            'ψ': 'psi', 'Ψ': 'Psi',
            '∂': 'partial', '∇': 'nabla',
            '⊗': 'tensor', '∮': 'contour',
            'Ξ': 'xi', 'Ω': 'omega', 'ω': 'omega_small',
            '∑': 'sum', '∫': 'integral',
            '⟦': 'semantic_open', '⟧': 'semantic_close',
            '∘': 'compose', '→': 'arrow', '↔': 'bidir',
            '¬': 'not', '∞': 'infinity'
        }

        # Composition patterns
        self.composition_pattern = re.compile(
            r'([φΦψΨ∂∇⊗∮ΞΩω])\s*[∘○◦]\s*([φΦψΨ∂∇⊗∮ΞΩω])'
        )

        # Equation patterns
        self.equation_pattern = re.compile(
            r'[φΦψΨ∂∇⊗∮ΞΩωλΛμνρσταβγδεζηθικμξπστυχ][^.!?]*?[=≈≡→↔]'
        )

        # Contradiction keywords
        self.contradiction_keywords = [
            'paradox', 'contradiction', 'contradictory',
            "J'≠0", "J'", 'J=0', 'J = 0',
            'both...and not', 'simultaneously',
            'rupture', 'collapse', 'void'
        ]

    def extract_from_file(self, file_path: Path) -> Dict:
        """Extract all patterns from a single file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            return {'error': 'Could not read file'}

        result = {
            'file': str(file_path),
            'operators': self._extract_operators(content),
            'compositions': self._extract_compositions(content),
            'equations': self._extract_equations(content),
            'contradictions': self._extract_contradictions(content)
        }

        return result

    def _extract_operators(self, content: str) -> Dict:
        """Count operator frequencies"""
        counts = Counter()
        contexts = defaultdict(list)

        for symbol, name in self.operators.items():
            # Find all occurrences
            positions = [m.start() for m in re.finditer(re.escape(symbol), content)]
            counts[symbol] = len(positions)

            # Extract context (±50 chars)
            for pos in positions[:5]:  # Limit to 5 contexts per operator
                start = max(0, pos - 50)
                end = min(len(content), pos + 50)
                ctx = content[start:end].replace('\n', ' ')
                contexts[symbol].append(ctx)

        return {
            'frequencies': dict(counts),
            'contexts': {k: v for k, v in contexts.items() if v}
        }

    def _extract_compositions(self, content: str) -> List[str]:
        """Find operator compositions like φ ∘ ψ"""
        matches = self.composition_pattern.findall(content)
        compositions = [f"{op1} ∘ {op2}" for op1, op2 in matches]
        return list(set(compositions))  # Unique compositions

    def _extract_equations(self, content: str) -> List[Dict]:
        """Extract mathematical equations"""
        equations = []
        matches = self.equation_pattern.findall(content)

        for eq in matches[:20]:  # Limit to 20 per file
            # Clean up the equation
            eq_clean = ' '.join(eq.split())
            if len(eq_clean) > 10 and len(eq_clean) < 200:  # Reasonable length
                equations.append({
                    'text': eq_clean,
                    'operators': [op for op in self.operators.keys() if op in eq_clean]
                })

        return equations

    def _extract_contradictions(self, content: str) -> List[Dict]:
        """Find contradiction mentions"""
        contradictions = []

        for keyword in self.contradiction_keywords:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matches = pattern.finditer(content)

            for match in matches:
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end].replace('\n', ' ')

                contradictions.append({
                    'keyword': keyword,
                    'context': ' '.join(context.split())
                })

        return contradictions

def main():
    print("\n" + "="*70)
    print("PATTERN-BASED EXTRACTION (No API Required)")
    print("="*70 + "\n")

    # Find all markdown files
    repo_path = Path('.')
    md_files = list(repo_path.rglob('*.md'))

    # Exclude certain directories
    md_files = [f for f in md_files if 'extraction_outputs' not in str(f)]

    print(f"Found {len(md_files)} markdown files\n")
    print("Extracting patterns...")

    extractor = PatternExtractor()
    results = []

    # Process files with progress
    for i, file_path in enumerate(md_files, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(md_files)} files...")

        result = extractor.extract_from_file(file_path)
        if 'error' not in result:
            results.append(result)

    print(f"  Processed {len(md_files)}/{len(md_files)} files\n")

    # Save results
    output_dir = Path('extraction_outputs')
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / 'pattern_extraction.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Generate summary
    print("="*70)
    print("EXTRACTION SUMMARY")
    print("="*70)

    # Aggregate statistics
    total_operators = Counter()
    all_compositions = set()
    total_equations = 0
    total_contradictions = 0

    for result in results:
        for op, count in result['operators']['frequencies'].items():
            total_operators[op] += count
        all_compositions.update(result['compositions'])
        total_equations += len(result['equations'])
        total_contradictions += len(result['contradictions'])

    print(f"\nFiles processed: {len(results)}")
    print(f"\nTop 10 operators by frequency:")
    for op, count in total_operators.most_common(10):
        print(f"  {op}: {count:,}")

    print(f"\nUnique operator compositions found: {len(all_compositions)}")
    if all_compositions:
        print("Sample compositions:")
        for comp in list(all_compositions)[:10]:
            print(f"  {comp}")

    print(f"\nTotal equations extracted: {total_equations:,}")
    print(f"Total contradiction mentions: {total_contradictions:,}")

    print(f"\n✓ Results saved to: {output_file}")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
