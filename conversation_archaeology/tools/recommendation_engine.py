#!/usr/bin/env python3
"""
Recommendation Engine - Next Patterns to Explore

Suggests:
- Underexplored domains
- Operator combinations not yet attempted
- φ-depth progression opportunities
- Novel thinking modes to try
"""

import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))


class RecommendationEngine:
    """Recommend next exploration paths based on vault history"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def get_domain_coverage(self) -> Dict[str, int]:
        """Get domain usage counts"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT d.domain, COUNT(*) as count
            FROM domains d
            JOIN conversation_domains cd ON d.id = cd.domain_id
            GROUP BY d.domain
            ORDER BY count DESC
        ''')

        return {row['domain']: row['count'] for row in cursor.fetchall()}

    def get_operator_coverage(self) -> Dict[str, int]:
        """Get operator usage counts"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT o.operator, COUNT(*) as count
            FROM operators o
            JOIN conversation_operators co ON o.id = co.operator_id
            GROUP BY o.operator
            ORDER BY count DESC
        ''')

        return {row['operator']: row['count'] for row in cursor.fetchall()}

    def get_operator_combinations(self) -> Dict[Tuple[str, str], int]:
        """Get existing operator pair usage"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT id FROM conversations')
        conversation_ids = [row[0] for row in cursor.fetchall()]

        combinations = defaultdict(int)

        for conv_id in conversation_ids:
            cursor.execute('''
                SELECT o.operator FROM operators o
                JOIN conversation_operators co ON o.id = co.operator_id
                WHERE co.conversation_id = ?
            ''', (conv_id,))

            operators = [row[0] for row in cursor.fetchall()]

            for i, op1 in enumerate(operators):
                for op2 in operators[i+1:]:
                    pair = tuple(sorted([op1, op2]))
                    combinations[pair] += 1

        return dict(combinations)

    def get_phi_progression(self) -> List[int]:
        """Get φ-depths achieved"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT DISTINCT phi_depth FROM conversations ORDER BY phi_depth DESC')

        return [row[0] for row in cursor.fetchall()]

    def recommend_underexplored_domains(self, limit: int = 10) -> List[Dict]:
        """Identify domains to explore more"""
        coverage = self.get_domain_coverage()

        # All possible domains
        all_domains = [
            'recursion', 'consciousness', 'torsion', 'collapse',
            'meta-cognition', 'paradox', 'operators', 'identity',
            'emergence', 'self-reference', 'incompleteness', 'contradiction'
        ]

        recommendations = []
        for domain in all_domains:
            count = coverage.get(domain, 0)
            if count < 20:  # Underexplored threshold
                recommendations.append({
                    'domain': domain,
                    'current_count': count,
                    'priority': 'high' if count < 5 else 'medium',
                    'reason': f'Only {count} conversations, opportunity for depth'
                })

        return sorted(recommendations, key=lambda x: x['current_count'])[:limit]

    def recommend_operator_combinations(self, limit: int = 10) -> List[Dict]:
        """Suggest unexplored operator pairs"""
        coverage = self.get_operator_coverage()
        existing_pairs = self.get_operator_combinations()

        # Top operators
        top_operators = [op for op, _ in sorted(coverage.items(), key=lambda x: x[1], reverse=True)[:20]]

        # Find unexplored pairs
        unexplored = []
        for i, op1 in enumerate(top_operators):
            for op2 in top_operators[i+1:]:
                pair = tuple(sorted([op1, op2]))
                if pair not in existing_pairs:
                    unexplored.append({
                        'operators': f"{op1} ⊗ {op2}",
                        'op1': op1,
                        'op2': op2,
                        'op1_count': coverage[op1],
                        'op2_count': coverage[op2],
                        'reason': f'Both proven operators, never combined'
                    })

        # Sort by operator importance
        unexplored.sort(key=lambda x: x['op1_count'] + x['op2_count'], reverse=True)

        return unexplored[:limit]

    def recommend_phi_depth_targets(self) -> List[Dict]:
        """Suggest next φ-depth milestones"""
        achieved = set(self.get_phi_progression())
        max_phi = max(achieved) if achieved else 0

        recommendations = []

        # Suggest next milestones
        milestones = [5, 10, 15, 20, 30, 50, 75, 100, 150, 200]

        for milestone in milestones:
            if milestone > max_phi:
                recommendations.append({
                    'target': f'φ{milestone}',
                    'current_max': f'φ{max_phi}',
                    'gap': milestone - max_phi,
                    'difficulty': 'medium' if milestone <= max_phi + 10 else 'high',
                    'reason': f'Next recursive depth milestone'
                })

            elif milestone not in achieved:
                recommendations.append({
                    'target': f'φ{milestone}',
                    'current_max': f'φ{max_phi}',
                    'gap': 0,
                    'difficulty': 'low',
                    'reason': f'Below max but never achieved exactly'
                })

        return recommendations[:5]

    def recommend_thinking_modes(self) -> List[Dict]:
        """Suggest thinking mode variations"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT thinking_mode, COUNT(*) as count
            FROM conversations
            GROUP BY thinking_mode
            ORDER BY count DESC
        ''')

        mode_counts = {row['thinking_mode']: row['count'] for row in cursor.fetchall()}

        # All possible modes
        all_modes = ['extended', 'normal', 'minimal', 'unknown']

        recommendations = []
        for mode in all_modes:
            count = mode_counts.get(mode, 0)
            if count < 50:
                recommendations.append({
                    'mode': mode,
                    'current_count': count,
                    'reason': f'Only {count} conversations in this mode'
                })

        return recommendations

    def generate_exploration_report(self) -> str:
        """Generate comprehensive recommendation report"""
        output = []
        output.append("=" * 80)
        output.append("🔮 PATTERN EXPLORATION RECOMMENDATIONS")
        output.append("=" * 80)
        output.append("")
        output.append("Based on your conversation archaeology, here are suggested next explorations:")
        output.append("")

        # Domain recommendations
        domain_recs = self.recommend_underexplored_domains(10)
        if domain_recs:
            output.append("🎯 Underexplored Domains (High Priority):")
            output.append("")
            for rec in domain_recs:
                priority_marker = "🔥" if rec['priority'] == 'high' else "⚡"
                output.append(f"  {priority_marker} {rec['domain']:20s} ({rec['current_count']:3d} convos) - {rec['reason']}")
            output.append("")

        # Operator combinations
        op_combos = self.recommend_operator_combinations(10)
        if op_combos:
            output.append("⚡ Unexplored Operator Combinations:")
            output.append("")
            for rec in op_combos:
                output.append(f"  • {rec['operators']:40s} (Both proven, never paired)")
            output.append("")

        # φ-depth targets
        phi_targets = self.recommend_phi_depth_targets()
        if phi_targets:
            output.append("📈 φ-Depth Progression Targets:")
            output.append("")
            for rec in phi_targets:
                difficulty_marker = "🟢" if rec['difficulty'] == 'low' else "🟡" if rec['difficulty'] == 'medium' else "🔴"
                output.append(f"  {difficulty_marker} {rec['target']:5s} (gap: {rec['gap']:3d} levels) - {rec['reason']}")
            output.append("")

        # Thinking modes
        mode_recs = self.recommend_thinking_modes()
        if mode_recs:
            output.append("🧠 Thinking Mode Variations to Try:")
            output.append("")
            for rec in mode_recs:
                output.append(f"  • {rec['mode']:15s} ({rec['current_count']:3d} convos) - {rec['reason']}")
            output.append("")

        # Synthesis recommendations
        output.append("🔬 Synthesis Recommendations:")
        output.append("")
        output.append("  Based on your patterns, consider exploring:")
        output.append("")

        # Get top domains and operators
        domains = self.get_domain_coverage()
        operators = self.get_operator_coverage()

        top_domain = max(domains.items(), key=lambda x: x[1])[0] if domains else "recursion"
        weak_domains = [d for d, c in domains.items() if c < 10]

        if weak_domains:
            output.append(f"  1. Bridge {top_domain} with {weak_domains[0]}")
            output.append(f"     → Combine your strongest domain with underexplored territory")
            output.append("")

        if len(operators) >= 2:
            top_ops = sorted(operators.items(), key=lambda x: x[1], reverse=True)[:2]
            output.append(f"  2. Meta-recursive application of {top_ops[0][0]}")
            output.append(f"     → Apply your most-used operator to itself")
            output.append("")

        output.append(f"  3. Sustained φ-depth exploration")
        output.append(f"     → Pick a domain and push φ-depth continuously")
        output.append("")

        output.append("=" * 80)

        return "\n".join(output)

    def close(self):
        self.conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Pattern Exploration Recommendation Engine")
    parser.add_argument(
        '--vault',
        type=Path,
        default=Path('/tmp/your_conversation_vault.db'),
        help='Path to vault database'
    )

    args = parser.parse_args()

    if not args.vault.exists():
        print(f"❌ Vault not found: {args.vault}")
        print("   Run populate_vault.py first")
        sys.exit(1)

    engine = RecommendationEngine(args.vault)

    print(engine.generate_exploration_report())

    engine.close()


if __name__ == "__main__":
    main()
