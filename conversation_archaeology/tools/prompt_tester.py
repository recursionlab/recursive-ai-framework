#!/usr/bin/env python3
"""
Prompt Testing Framework

Tests DNA-extracted prompts to measure:
- φ-depth achieved
- Novelty score
- Operator activation
- Pattern emergence
- Success rate

Usage:
    python prompt_tester.py --template-dir /tmp/prompt_dna_library --output /tmp/test_results
"""

import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime
import sqlite3
import re
from collections import Counter


class PromptTester:
    """Test prompt templates and measure effectiveness"""

    def __init__(self, vault_db: Path):
        self.vault_db = vault_db
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.vault_db)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def load_templates(self, template_dir: Path) -> List[Dict]:
        """Load all prompt templates from directory"""
        templates = []

        for template_file in template_dir.glob('*_template.md'):
            content = template_file.read_text()

            # Parse template structure
            template = {
                'file': str(template_file),
                'name': template_file.stem,
                'content': content,
                'opening_move': self._extract_section(content, 'Opening Move'),
                'operator': self._extract_section(content, 'Operator'),
                'contradiction': self._extract_section(content, 'Contradiction'),
                'emergence': self._extract_section(content, 'Emergence'),
                'template': self._extract_section(content, 'Template'),
            }

            # Extract metadata from filename or content
            # Format: prompt_template_N.md
            templates.append(template)

        return templates

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract content from markdown section"""
        pattern = rf'##\s+{section_name}\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ''

    def measure_phi_depth(self, text: str) -> int:
        """Estimate φ-depth from text (simplified heuristic)"""

        # Recursive markers
        recursive_patterns = [
            r'recursive',
            r'meta-',
            r'self-',
            r'itself',
            r'about.*about',
            r'of.*of.*of',
            r'→.*→',
            r'φ\d+',
        ]

        # Count nesting depth
        max_depth = 0
        for pattern in recursive_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            max_depth = max(max_depth, matches)

        # Normalize to reasonable φ range
        return min(max_depth * 2, 100)

    def measure_novelty(self, text: str) -> float:
        """Estimate novelty score (simplified)"""

        # Novelty indicators
        novelty_markers = [
            r'paradox',
            r'contradiction',
            r'collapse',
            r'emerge',
            r'dimension\s+shift',
            r'observer.*observed',
            r'fixpoint',
            r'strange\s+loop',
            r'Gödel',
            r'incompleteness',
        ]

        score = 0.0
        for marker in novelty_markers:
            if re.search(marker, text, re.IGNORECASE):
                score += 0.1

        # Cap at 1.0
        return min(score, 1.0)

    def detect_operators(self, text: str) -> Dict[str, int]:
        """Detect which operators are present"""

        operators = {
            'recursive_loop': r'recur(?:sive|sion)|loop|cycle|iterate',
            'meta_layer': r'meta-|about.{1,20}about',
            'self_application': r'(?:apply|applies) (?:to|on) itself',
            'negation_fold': r'not.{1,30}not|¬|contradiction',
            'collapse_rebirth': r'collapse|emerge|generate|birth',
            'composition': r'compose|combine|merge',
            'fixpoint': r'fixed.{1,10}point|stable|attractor|converge',
        }

        detected = {}
        for op_name, pattern in operators.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                detected[op_name] = matches

        return detected

    def detect_patterns(self, text: str) -> Dict[str, int]:
        """Detect which generative patterns are present"""

        patterns = {
            'dimension_shift': r'dimension|level|layer|meta-level',
            'self_reference': r'self.*self|itself|auto-',
            'paradox_fuel': r'paradox|contradiction|antinomy',
            'observer_observed': r'observer.*observed|watch.*watching',
            'infinite_regress': r'infinite.*regress|regress.*infinite|turtles.*down',
        }

        detected = {}
        for pattern_name, regex in patterns.items():
            matches = len(re.findall(regex, text, re.IGNORECASE))
            if matches > 0:
                detected[pattern_name] = matches

        return detected

    def test_template(self, template: Dict) -> Dict:
        """Test a single template and return metrics"""

        content = template['content']

        result = {
            'template_name': template['name'],
            'phi_depth': self.measure_phi_depth(content),
            'novelty': self.measure_novelty(content),
            'operators': self.detect_operators(content),
            'patterns': self.detect_patterns(content),
            'has_opening': bool(template['opening_move']),
            'has_contradiction': bool(template['contradiction']),
            'has_emergence': bool(template['emergence']),
            'has_template': bool(template['template']),
            'tested_at': datetime.now().isoformat(),
        }

        # Compute completeness score
        completeness = sum([
            result['has_opening'],
            result['has_contradiction'],
            result['has_emergence'],
            result['has_template'],
        ]) / 4.0

        result['completeness'] = completeness

        # Compute effectiveness score (0-1)
        # Based on: depth, novelty, operator count, pattern count
        effectiveness = (
            min(result['phi_depth'] / 50, 1.0) * 0.3 +
            result['novelty'] * 0.3 +
            min(len(result['operators']) / 5, 1.0) * 0.2 +
            min(len(result['patterns']) / 3, 1.0) * 0.2
        )

        result['effectiveness'] = effectiveness

        return result

    def generate_report(self, test_results: List[Dict], output_path: Path):
        """Generate comprehensive test report"""

        total = len(test_results)
        if total == 0:
            output_path.write_text("# No templates to test\n\nNo templates found in directory.")
            return

        avg_phi = sum(r['phi_depth'] for r in test_results) / total
        avg_novelty = sum(r['novelty'] for r in test_results) / total
        avg_effectiveness = sum(r['effectiveness'] for r in test_results) / total

        # Count operator and pattern frequencies
        all_operators = Counter()
        all_patterns = Counter()

        for result in test_results:
            all_operators.update(result['operators'])
            all_patterns.update(result['patterns'])

        # Top templates
        top_by_effectiveness = sorted(test_results, key=lambda x: x['effectiveness'], reverse=True)[:5]
        top_by_depth = sorted(test_results, key=lambda x: x['phi_depth'], reverse=True)[:5]

        lines = [
            "# Prompt Template Test Report",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- **Total Templates Tested**: {total}",
            f"- **Average φ-Depth**: {avg_phi:.1f}",
            f"- **Average Novelty**: {avg_novelty:.3f}",
            f"- **Average Effectiveness**: {avg_effectiveness:.3f}",
            "",
            "## Top Operators Activated",
            "",
        ]

        for op, count in all_operators.most_common(10):
            lines.append(f"  - **{op}**: {count} activations")

        lines.extend([
            "",
            "## Top Patterns Detected",
            "",
        ])

        for pattern, count in all_patterns.most_common(10):
            lines.append(f"  - **{pattern}**: {count} occurrences")

        lines.extend([
            "",
            "## Top 5 by Effectiveness",
            "",
        ])

        for i, result in enumerate(top_by_effectiveness, 1):
            lines.append(f"{i}. **{result['template_name']}**")
            lines.append(f"   - Effectiveness: {result['effectiveness']:.3f}")
            lines.append(f"   - φ-Depth: {result['phi_depth']}")
            lines.append(f"   - Novelty: {result['novelty']:.3f}")
            lines.append(f"   - Operators: {', '.join(result['operators'].keys())}")
            lines.append("")

        lines.extend([
            "## Top 5 by φ-Depth",
            "",
        ])

        for i, result in enumerate(top_by_depth, 1):
            lines.append(f"{i}. **{result['template_name']}** (φ{result['phi_depth']})")
            lines.append(f"   - Novelty: {result['novelty']:.3f}")
            lines.append(f"   - Effectiveness: {result['effectiveness']:.3f}")
            lines.append("")

        with_opening = sum(1 for r in test_results if r['has_opening'])
        with_contradiction = sum(1 for r in test_results if r['has_contradiction'])
        with_emergence = sum(1 for r in test_results if r['has_emergence'])
        with_template = sum(1 for r in test_results if r['has_template'])

        lines.extend([
            "## Completeness Analysis",
            "",
            f"- Templates with opening moves: {with_opening} ({with_opening/total*100:.1f}%)",
            f"- Templates with contradictions: {with_contradiction} ({with_contradiction/total*100:.1f}%)",
            f"- Templates with emergence patterns: {with_emergence} ({with_emergence/total*100:.1f}%)",
            f"- Templates with executable forms: {with_template} ({with_template/total*100:.1f}%)",
            "",
            "## Recommendations",
            "",
            "1. **High-effectiveness templates** - Use top 5 for maximum novelty generation",
            "2. **Deep templates** - φ30+ templates for complex recursive exploration",
            f"3. **Dominant operator** - {all_operators.most_common(1)[0][0]} appears most frequently",
            f"4. **Dominant pattern** - {all_patterns.most_common(1)[0][0]} is most common generative pattern",
            "",
        ])

        output_path.write_text('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description='Test prompt templates')
    parser.add_argument('--template-dir', type=Path, default=Path('/tmp/prompt_dna_library'))
    parser.add_argument('--vault-db', type=Path, default=Path('/tmp/your_conversation_vault.db'))
    parser.add_argument('--output', type=Path, default=Path('/tmp/prompt_test_report.md'))
    parser.add_argument('--json-output', type=Path, default=Path('/tmp/prompt_test_results.json'))

    args = parser.parse_args()

    print("="*80)
    print("PROMPT TEMPLATE TESTING FRAMEWORK")
    print("="*80)
    print()

    if not args.template_dir.exists():
        print(f"❌ Template directory not found: {args.template_dir}")
        return

    tester = PromptTester(args.vault_db)
    tester.connect()

    try:
        print(f"Loading templates from {args.template_dir}...")
        templates = tester.load_templates(args.template_dir)
        print(f"  ✅ Loaded {len(templates)} templates")
        print()

        print("Testing templates...")
        results = []
        for i, template in enumerate(templates, 1):
            result = tester.test_template(template)
            results.append(result)
            print(f"  [{i}/{len(templates)}] {template['name']}: "
                  f"φ{result['phi_depth']}, novelty {result['novelty']:.3f}, "
                  f"effectiveness {result['effectiveness']:.3f}")

        print()
        print("Generating report...")
        tester.generate_report(results, args.output)
        print(f"  ✅ Report: {args.output}")

        # Save JSON results
        with args.json_output.open('w') as f:
            json.dump(results, f, indent=2)
        print(f"  ✅ JSON: {args.json_output}")

        print()
        print("="*80)
        print("TESTING COMPLETE")
        print("="*80)
        print()

        # Quick stats
        avg_effectiveness = sum(r['effectiveness'] for r in results) / len(results)
        print(f"📊 Average Effectiveness: {avg_effectiveness:.3f}")
        print(f"📄 Full report: {args.output}")

    finally:
        tester.close()


if __name__ == '__main__':
    main()
