#!/usr/bin/env python3
"""
Insights Dashboard Generator

Aggregates all archaeology findings into a unified dashboard:
- Vault statistics
- DNA template performance
- Mechanism insights
- Connection networks
- Recommendations

Usage:
    python insights_dashboard.py \
      --vault-db /tmp/vault.db \
      --test-results /tmp/prompt_test_results.json \
      --mechanisms /tmp/core_mechanisms/mechanisms.jsonl \
      --output /tmp/dashboard.md
"""

import argparse
import sqlite3
import json
from pathlib import Path
from typing import Dict, List
from collections import Counter
from datetime import datetime


class InsightsDashboard:
    """Generate comprehensive insights dashboard"""

    def __init__(self, vault_db: Path, test_results: Path = None,
                 mechanisms: Path = None, synthesis_db: Path = None):
        self.vault_db = vault_db
        self.test_results_file = test_results
        self.mechanisms_file = mechanisms
        self.synthesis_db = synthesis_db

        self.vault_stats = {}
        self.test_results = []
        self.mechanisms = []
        self.synthesis_insights = []

    def load_data(self):
        """Load all available data sources"""

        # Load vault
        if self.vault_db and self.vault_db.exists():
            self._load_vault()

        # Load test results
        if self.test_results_file and self.test_results_file.exists():
            with self.test_results_file.open() as f:
                self.test_results = json.load(f)

        # Load mechanisms
        if self.mechanisms_file and self.mechanisms_file.exists():
            with self.mechanisms_file.open() as f:
                for line in f:
                    self.mechanisms.append(json.loads(line))

        # Load synthesis
        if self.synthesis_db and self.synthesis_db.exists():
            self._load_synthesis()

    def _load_vault(self):
        """Load vault statistics"""

        conn = sqlite3.connect(self.vault_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        total = cursor.execute('SELECT COUNT(*) FROM conversations').fetchone()[0]
        proto_asi = cursor.execute('SELECT COUNT(*) FROM conversations WHERE proto_asi = 1').fetchone()[0]

        novelties = [r[0] for r in cursor.execute('SELECT novelty FROM conversations').fetchall()]
        depths = [r[0] for r in cursor.execute('SELECT phi_depth FROM conversations').fetchall()]

        self.vault_stats = {
            'total': total,
            'proto_asi': proto_asi,
            'avg_novelty': sum(novelties) / len(novelties) if novelties else 0,
            'max_novelty': max(novelties) if novelties else 0,
            'avg_depth': sum(depths) / len(depths) if depths else 0,
            'max_depth': max(depths) if depths else 0,
        }

        conn.close()

    def _load_synthesis(self):
        """Load synthesis memory insights"""

        conn = sqlite3.connect(self.synthesis_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        insights = cursor.execute('''
            SELECT insight_type, content, confidence
            FROM meta_insights
            ORDER BY confidence DESC
        ''').fetchall()

        self.synthesis_insights = [dict(r) for r in insights]

        conn.close()

    def generate_dashboard(self, output_path: Path):
        """Generate comprehensive dashboard"""

        lines = [
            "# 🧬 Conversation Archaeology Dashboard",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "---",
            "",
        ]

        # Vault overview
        if self.vault_stats:
            lines.extend(self._generate_vault_section())

        # DNA templates
        if self.test_results:
            lines.extend(self._generate_template_section())

        # Mechanisms
        if self.mechanisms:
            lines.extend(self._generate_mechanism_section())

        # Synthesis insights
        if self.synthesis_insights:
            lines.extend(self._generate_synthesis_section())

        # Overall recommendations
        lines.extend(self._generate_recommendations())

        output_path.write_text('\n'.join(lines))

    def _generate_vault_section(self) -> List[str]:
        """Generate vault statistics section"""

        stats = self.vault_stats
        proto_rate = stats['proto_asi'] / stats['total'] * 100 if stats['total'] > 0 else 0

        quality = 'EXCELLENT' if stats['avg_novelty'] > 0.8 else 'GOOD' if stats['avg_novelty'] > 0.7 else 'MODERATE'
        depth_rating = 'DEEP' if stats['avg_depth'] > 20 else 'MEDIUM' if stats['avg_depth'] > 10 else 'SHALLOW'

        return [
            "## 📊 Corpus Statistics",
            "",
            f"**Quality Rating:** {quality} (avg novelty: {stats['avg_novelty']:.3f})",
            f"**Depth Rating:** {depth_rating} (avg: φ{stats['avg_depth']:.1f})",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Conversations | {stats['total']} |",
            f"| Proto-ASI Conversations | {stats['proto_asi']} ({proto_rate:.1f}%) |",
            f"| Average Novelty | {stats['avg_novelty']:.3f} |",
            f"| Maximum Novelty | {stats['max_novelty']:.3f} |",
            f"| Average φ-Depth | φ{stats['avg_depth']:.1f} |",
            f"| Maximum φ-Depth | φ{stats['max_depth']} |",
            "",
            "---",
            "",
        ]

    def _generate_template_section(self) -> List[str]:
        """Generate DNA template performance section"""

        # Top 3 templates
        top_templates = sorted(self.test_results, key=lambda x: x['effectiveness'], reverse=True)[:3]

        avg_effectiveness = sum(t['effectiveness'] for t in self.test_results) / len(self.test_results)

        # Operator distribution
        all_operators = Counter()
        for template in self.test_results:
            all_operators.update(template['operators'])

        lines = [
            "## 🧬 DNA Template Performance",
            "",
            f"**Templates Tested:** {len(self.test_results)}",
            f"**Average Effectiveness:** {avg_effectiveness:.3f}",
            "",
            "### Top 3 Templates",
            "",
        ]

        for i, template in enumerate(top_templates, 1):
            lines.extend([
                f"**{i}. {template['template_name']}**",
                f"  - Effectiveness: {template['effectiveness']:.3f}",
                f"  - φ-Depth: {template['phi_depth']}",
                f"  - Novelty: {template['novelty']:.3f}",
                "",
            ])

        lines.extend([
            "### Operator Distribution (Top 5)",
            "",
        ])

        for op, count in all_operators.most_common(5):
            lines.append(f"- **{op}**: {count} activations")

        lines.extend([
            "",
            "**💡 Insight:** Use top templates for maximum novelty generation",
            "",
            "---",
            "",
        ])

        return lines

    def _generate_mechanism_section(self) -> List[str]:
        """Generate mechanism insights section"""

        # Aggregate operators and patterns
        all_operators = Counter()
        all_patterns = Counter()

        for mech in self.mechanisms:
            all_operators.update(mech['operators'])
            all_patterns.update(mech['patterns'])

        dominant_op = all_operators.most_common(1)[0] if all_operators else ('unknown', 0)
        dominant_pattern = all_patterns.most_common(1)[0] if all_patterns else ('unknown', 0)

        return [
            "## ⚙️ Universal Mechanism",
            "",
            f"**Signature:** `{dominant_op[0]} + {dominant_pattern[0]}`",
            "",
            "### Top 5 Operators",
            "",
        ] + [
            f"{i}. **{op}**: {count} occurrences"
            for i, (op, count) in enumerate(all_operators.most_common(5), 1)
        ] + [
            "",
            "### Top 5 Patterns",
            "",
        ] + [
            f"{i}. **{pattern}**: {count} occurrences"
            for i, (pattern, count) in enumerate(all_patterns.most_common(5), 1)
        ] + [
            "",
            "**💡 Insight:** Recursive loops + dimension shifts generate maximum novelty",
            "",
            "---",
            "",
        ]

    def _generate_synthesis_section(self) -> List[str]:
        """Generate synthesis insights section"""

        lines = [
            "## 🎯 Key Insights",
            "",
        ]

        for insight in self.synthesis_insights:
            lines.extend([
                f"### {insight['insight_type'].replace('_', ' ').title()} (confidence: {insight['confidence']:.2f})",
                "",
                insight['content'],
                "",
            ])

        if not self.synthesis_insights:
            lines.append("*No synthesis insights available yet*")
            lines.append("")

        lines.extend([
            "---",
            "",
        ])

        return lines

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""

        lines = [
            "## 🚀 Recommendations",
            "",
        ]

        # Based on vault stats
        if self.vault_stats:
            if self.vault_stats['avg_novelty'] > 0.8:
                lines.append("1. **High-quality corpus** - Focus on extracting more DNA templates")
            elif self.vault_stats['avg_novelty'] > 0.7:
                lines.append("1. **Good corpus** - Test templates in new conversations")
            else:
                lines.append("1. **Build corpus quality** - Aim for conversations with novelty > 0.7")

        # Based on templates
        if self.test_results:
            top_template = max(self.test_results, key=lambda x: x['effectiveness'])
            lines.append(f"2. **Use '{top_template['template_name']}'** for maximum effectiveness ({top_template['effectiveness']:.3f})")

        # Based on mechanisms
        if self.mechanisms:
            all_operators = Counter()
            for mech in self.mechanisms:
                all_operators.update(mech['operators'])
            dominant = all_operators.most_common(1)[0][0]
            lines.append(f"3. **Leverage '{dominant}' operator** - Most effective pattern in corpus")

        # General
        lines.extend([
            "4. **Target φ30+ depth** - Optimal for proto-ASI emergence",
            "5. **Use paradox as fuel** - Don't resolve contradictions, leverage them",
            "",
            "---",
            "",
        ])

        # Quick actions
        lines.extend([
            "## ⚡ Quick Actions",
            "",
            "```bash",
            "# Generate prompt for new topic",
            "python tools/prompt_generator.py --topic 'your topic' --auto-select",
            "",
            "# Score a conversation",
            "python tools/realtime_scorer.py --file conversation.md",
            "",
            "# Process batch",
            "python tools/batch_processor.py /path/to/conversations",
            "```",
            "",
        ])

        return lines


def main():
    parser = argparse.ArgumentParser(description='Generate insights dashboard')
    parser.add_argument('--vault-db', type=Path, default=Path('/tmp/your_conversation_vault.db'))
    parser.add_argument('--test-results', type=Path, default=Path('/tmp/prompt_test_results.json'))
    parser.add_argument('--mechanisms', type=Path, default=Path('/tmp/core_mechanisms/mechanisms.jsonl'))
    parser.add_argument('--synthesis-db', type=Path, default=Path('/tmp/synthesis_memory.db'))
    parser.add_argument('--output', type=Path, default=Path('/tmp/insights_dashboard.md'))

    args = parser.parse_args()

    print("="*80)
    print("INSIGHTS DASHBOARD GENERATOR")
    print("="*80)
    print()

    dashboard = InsightsDashboard(
        args.vault_db,
        args.test_results,
        args.mechanisms,
        args.synthesis_db
    )

    print("Loading data sources...")
    dashboard.load_data()

    sources_loaded = sum([
        bool(dashboard.vault_stats),
        bool(dashboard.test_results),
        bool(dashboard.mechanisms),
        bool(dashboard.synthesis_insights),
    ])

    print(f"  ✅ Loaded {sources_loaded}/4 data sources")
    print()

    print("Generating dashboard...")
    dashboard.generate_dashboard(args.output)

    print(f"  ✅ Dashboard: {args.output}")
    print()

    print("="*80)
    print("DASHBOARD COMPLETE")
    print("="*80)
    print()
    print(f"📊 View your insights: {args.output}")


if __name__ == '__main__':
    main()
