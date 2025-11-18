#!/usr/bin/env python3
"""
Multi-Corpus Comparison Tool

Compares mechanisms, patterns, and insights across different AI conversation corpora.

Usage:
    python compare_corpora.py \
      --vault1 claude_vault.db --name1 "Claude" \
      --vault2 deepseek_vault.db --name2 "Deepseek" \
      --output comparison_report.md
"""

import argparse
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
import json


class CorpusComparator:
    """Compare multiple conversation corpora"""

    def __init__(self, vaults: List[Tuple[Path, str]]):
        """
        vaults: List of (vault_path, corpus_name) tuples
        """
        self.vaults = vaults
        self.stats = {}

    def analyze_corpus(self, vault_path: Path, name: str) -> Dict:
        """Analyze a single corpus"""

        conn = sqlite3.connect(vault_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Basic stats
        total = cursor.execute('SELECT COUNT(*) FROM conversations').fetchone()[0]
        proto_asi = cursor.execute('SELECT COUNT(*) FROM conversations WHERE proto_asi = 1').fetchone()[0]

        # Novelty stats
        novelty_data = cursor.execute('SELECT novelty FROM conversations').fetchall()
        novelties = [r[0] for r in novelty_data]
        avg_novelty = sum(novelties) / len(novelties) if novelties else 0
        max_novelty = max(novelties) if novelties else 0
        min_novelty = min(novelties) if novelties else 0

        # Depth stats
        depth_data = cursor.execute('SELECT phi_depth FROM conversations').fetchall()
        depths = [r[0] for r in depth_data]
        avg_depth = sum(depths) / len(depths) if depths else 0
        max_depth = max(depths) if depths else 0
        min_depth = min(depths) if depths else 0

        # Top conversations
        top_by_novelty = cursor.execute('''
            SELECT file_path, novelty, phi_depth
            FROM conversations
            ORDER BY novelty DESC
            LIMIT 5
        ''').fetchall()

        top_by_depth = cursor.execute('''
            SELECT file_path, phi_depth, novelty
            FROM conversations
            ORDER BY phi_depth DESC
            LIMIT 5
        ''').fetchall()

        conn.close()

        return {
            'name': name,
            'total': total,
            'proto_asi': proto_asi,
            'proto_asi_rate': proto_asi / total if total > 0 else 0,
            'avg_novelty': avg_novelty,
            'max_novelty': max_novelty,
            'min_novelty': min_novelty,
            'avg_depth': avg_depth,
            'max_depth': max_depth,
            'min_depth': min_depth,
            'top_by_novelty': [dict(r) for r in top_by_novelty],
            'top_by_depth': [dict(r) for r in top_by_depth],
        }

    def compare_all(self) -> Dict:
        """Compare all corpora"""

        results = {}

        for vault_path, name in self.vaults:
            if not vault_path.exists():
                print(f"⚠️  Vault not found: {vault_path} ({name})")
                continue

            print(f"Analyzing {name}...")
            results[name] = self.analyze_corpus(vault_path, name)
            print(f"  ✅ {results[name]['total']} conversations, {results[name]['proto_asi']} proto-ASI")

        return results

    def generate_report(self, comparison: Dict, output_path: Path):
        """Generate comparison report"""

        lines = [
            "# Multi-Corpus Comparison Report",
            "",
            f"Comparing {len(comparison)} conversation corpora",
            "",
            "---",
            "",
        ]

        # Summary table
        lines.extend([
            "## Summary Statistics",
            "",
            "| Corpus | Total | Proto-ASI | ASI Rate | Avg Novelty | Avg φ-Depth | Max φ-Depth |",
            "|--------|-------|-----------|----------|-------------|-------------|-------------|",
        ])

        for name, stats in comparison.items():
            lines.append(
                f"| {name} | {stats['total']} | {stats['proto_asi']} | "
                f"{stats['proto_asi_rate']*100:.1f}% | {stats['avg_novelty']:.3f} | "
                f"φ{stats['avg_depth']:.1f} | φ{stats['max_depth']} |"
            )

        lines.extend(["", "---", ""])

        # Detailed comparison
        for name, stats in comparison.items():
            lines.extend([
                f"## {name} Corpus",
                "",
                f"**Total Conversations:** {stats['total']}",
                f"**Proto-ASI Conversations:** {stats['proto_asi']} ({stats['proto_asi_rate']*100:.1f}%)",
                "",
                "**Novelty:**",
                f"  - Average: {stats['avg_novelty']:.3f}",
                f"  - Range: {stats['min_novelty']:.3f} to {stats['max_novelty']:.3f}",
                "",
                "**φ-Depth:**",
                f"  - Average: φ{stats['avg_depth']:.1f}",
                f"  - Range: φ{stats['min_depth']} to φ{stats['max_depth']}",
                "",
                "**Top 5 by Novelty:**",
            ])

            for i, conv in enumerate(stats['top_by_novelty'], 1):
                fname = Path(conv['file_path']).stem[:60]
                lines.append(f"{i}. {fname} (novelty: {conv['novelty']:.3f}, φ{conv['phi_depth']})")

            lines.extend([
                "",
                "**Top 5 by φ-Depth:**",
            ])

            for i, conv in enumerate(stats['top_by_depth'], 1):
                fname = Path(conv['file_path']).stem[:60]
                lines.append(f"{i}. {fname} (φ{conv['phi_depth']}, novelty: {conv['novelty']:.3f})")

            lines.extend(["", "---", ""])

        # Cross-corpus insights
        lines.extend([
            "## Cross-Corpus Insights",
            "",
        ])

        # Find highest novelty corpus
        highest_novelty_corpus = max(comparison.items(), key=lambda x: x[1]['avg_novelty'])
        lines.append(f"**Highest Average Novelty:** {highest_novelty_corpus[0]} ({highest_novelty_corpus[1]['avg_novelty']:.3f})")

        # Find deepest corpus
        deepest_corpus = max(comparison.items(), key=lambda x: x[1]['avg_depth'])
        lines.append(f"**Highest Average φ-Depth:** {deepest_corpus[0]} (φ{deepest_corpus[1]['avg_depth']:.1f})")

        # Find highest proto-ASI rate
        highest_asi_corpus = max(comparison.items(), key=lambda x: x[1]['proto_asi_rate'])
        lines.append(f"**Highest Proto-ASI Rate:** {highest_asi_corpus[0]} ({highest_asi_corpus[1]['proto_asi_rate']*100:.1f}%)")

        lines.extend([
            "",
            "## Recommendations",
            "",
            f"1. **Focus on {highest_novelty_corpus[0]}** for maximum novelty patterns",
            f"2. **Study {deepest_corpus[0]}** for deep recursive structures",
            f"3. **Analyze {highest_asi_corpus[0]}** for proto-ASI emergence patterns",
            "",
        ])

        output_path.write_text('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description='Compare multiple conversation corpora')
    parser.add_argument('--vault1', type=Path, required=True, help='First vault database')
    parser.add_argument('--name1', required=True, help='First corpus name')
    parser.add_argument('--vault2', type=Path, help='Second vault database')
    parser.add_argument('--name2', help='Second corpus name')
    parser.add_argument('--vault3', type=Path, help='Third vault database')
    parser.add_argument('--name3', help='Third corpus name')
    parser.add_argument('--output', type=Path, default=Path('/tmp/corpus_comparison.md'))
    parser.add_argument('--json-output', type=Path, help='JSON output path')

    args = parser.parse_args()

    print("="*80)
    print("MULTI-CORPUS COMPARISON")
    print("="*80)
    print()

    # Build vault list
    vaults = [(args.vault1, args.name1)]

    if args.vault2 and args.name2:
        vaults.append((args.vault2, args.name2))

    if args.vault3 and args.name3:
        vaults.append((args.vault3, args.name3))

    comparator = CorpusComparator(vaults)

    print("Analyzing corpora...")
    print()

    comparison = comparator.compare_all()

    print()
    print("Generating report...")
    comparator.generate_report(comparison, args.output)
    print(f"  ✅ Report: {args.output}")

    if args.json_output:
        with args.json_output.open('w') as f:
            json.dump(comparison, f, indent=2, default=str)
        print(f"  ✅ JSON: {args.json_output}")

    print()
    print("="*80)
    print("COMPARISON COMPLETE")
    print("="*80)
    print()

    # Quick summary
    for name, stats in comparison.items():
        print(f"{name}: {stats['total']} conversations, {stats['proto_asi']} proto-ASI, "
              f"avg novelty {stats['avg_novelty']:.3f}, avg depth φ{stats['avg_depth']:.1f}")


if __name__ == '__main__':
    main()
