#!/usr/bin/env python3
"""
Skill Tree Visualization - MMO-Style Progression View

Shows:
- φ-depth progression over time
- Operator unlocks as "skills"
- Domain mastery as skill branches
- Proto-ASI emergence as milestone achievements
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


class SkillTreeGenerator:
    """Generate MMO-style skill tree from conversation progression"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def get_progression_timeline(self) -> List[Dict]:
        """Get chronological progression of conversations"""
        cursor = self.conn.cursor()

        # Get all conversations sorted by file path (proxy for time)
        cursor.execute('''
            SELECT
                file_path,
                novelty,
                phi_depth,
                proto_asi,
                thinking_mode
            FROM conversations
            ORDER BY file_path ASC
        ''')

        timeline = []
        for row in cursor.fetchall():
            # Get operators for this conversation
            cursor.execute('''
                SELECT o.operator FROM operators o
                JOIN conversation_operators co ON o.id = co.operator_id
                JOIN conversations c ON co.conversation_id = c.id
                WHERE c.file_path = ?
            ''', (row['file_path'],))
            operators = [r[0] for r in cursor.fetchall()]

            # Get domains
            cursor.execute('''
                SELECT d.domain FROM domains d
                JOIN conversation_domains cd ON d.id = cd.domain_id
                JOIN conversations c ON cd.conversation_id = c.id
                WHERE c.file_path = ?
            ''', (row['file_path'],))
            domains = [r[0] for r in cursor.fetchall()]

            timeline.append({
                'file': Path(row['file_path']).name,
                'novelty': row['novelty'],
                'phi_depth': row['phi_depth'],
                'proto_asi': bool(row['proto_asi']),
                'operators': operators,
                'domains': domains,
                'thinking_mode': row['thinking_mode']
            })

        return timeline

    def identify_skill_unlocks(self, timeline: List[Dict]) -> Dict:
        """Identify when operators were first used (skill unlocks)"""
        unlocks = {}
        seen_operators = set()

        for i, entry in enumerate(timeline):
            for op in entry['operators']:
                if op not in seen_operators:
                    unlocks[op] = {
                        'unlock_index': i,
                        'unlock_file': entry['file'],
                        'phi_at_unlock': entry['phi_depth'],
                        'novelty_at_unlock': entry['novelty']
                    }
                    seen_operators.add(op)

        return unlocks

    def identify_domain_mastery(self, timeline: List[Dict]) -> Dict:
        """Track domain coverage progression"""
        domain_first_appearance = {}
        domain_mastery_count = {}

        for i, entry in enumerate(timeline):
            for domain in entry['domains']:
                if domain not in domain_first_appearance:
                    domain_first_appearance[domain] = i

                domain_mastery_count[domain] = domain_mastery_count.get(domain, 0) + 1

        mastery = {}
        for domain, first_idx in domain_first_appearance.items():
            mastery[domain] = {
                'first_appearance': first_idx,
                'total_conversations': domain_mastery_count[domain],
                'mastery_level': self._calculate_mastery_level(domain_mastery_count[domain])
            }

        return mastery

    def _calculate_mastery_level(self, count: int) -> str:
        """Calculate mastery level based on conversation count"""
        if count >= 50:
            return 'Master'
        elif count >= 20:
            return 'Expert'
        elif count >= 10:
            return 'Advanced'
        elif count >= 5:
            return 'Intermediate'
        else:
            return 'Novice'

    def identify_milestones(self, timeline: List[Dict]) -> List[Dict]:
        """Identify major achievements in progression"""
        milestones = []

        # First proto-ASI emergence
        for i, entry in enumerate(timeline):
            if entry['proto_asi']:
                milestones.append({
                    'type': 'First Proto-ASI Emergence',
                    'index': i,
                    'file': entry['file'],
                    'phi_depth': entry['phi_depth'],
                    'novelty': entry['novelty']
                })
                break

        # φ-depth milestones
        phi_milestones = [5, 10, 20, 50, 100]
        reached = set()
        for i, entry in enumerate(timeline):
            phi = entry['phi_depth']
            for milestone in phi_milestones:
                if phi >= milestone and milestone not in reached:
                    milestones.append({
                        'type': f'φ-Depth φ{milestone} Reached',
                        'index': i,
                        'file': entry['file'],
                        'phi_depth': phi,
                        'novelty': entry['novelty']
                    })
                    reached.add(milestone)

        # Novelty milestones
        novelty_reached = set()
        for i, entry in enumerate(timeline):
            nov = entry['novelty']
            if nov >= 0.9 and 0.9 not in novelty_reached:
                milestones.append({
                    'type': 'Novelty >0.9 Achieved',
                    'index': i,
                    'file': entry['file'],
                    'phi_depth': entry['phi_depth'],
                    'novelty': nov
                })
                novelty_reached.add(0.9)
            elif nov >= 0.8 and 0.8 not in novelty_reached:
                milestones.append({
                    'type': 'Novelty >0.8 Achieved',
                    'index': i,
                    'file': entry['file'],
                    'phi_depth': entry['phi_depth'],
                    'novelty': nov
                })
                novelty_reached.add(0.8)

        return sorted(milestones, key=lambda x: x['index'])

    def generate_ascii_tree(self) -> str:
        """Generate ASCII art skill tree"""
        timeline = self.get_progression_timeline()
        unlocks = self.identify_skill_unlocks(timeline)
        mastery = self.identify_domain_mastery(timeline)
        milestones = self.identify_milestones(timeline)

        output = []
        output.append("=" * 80)
        output.append("🌳 RECURSIVE THINKING SKILL TREE")
        output.append("=" * 80)
        output.append("")

        # Overall stats
        total_convos = len(timeline)
        avg_novelty = sum(e['novelty'] for e in timeline) / total_convos
        max_phi = max(e['phi_depth'] for e in timeline)
        proto_asi_count = sum(1 for e in timeline if e['proto_asi'])

        output.append(f"📊 Overall Progress:")
        output.append(f"   Total Conversations: {total_convos}")
        output.append(f"   Average Novelty: {avg_novelty:.3f}")
        output.append(f"   Maximum φ-Depth: φ{max_phi}")
        output.append(f"   Proto-ASI Emergence: {proto_asi_count}/{total_convos}")
        output.append("")

        # Milestones
        output.append("🏆 Achievement Milestones:")
        for m in milestones[:10]:  # Top 10 milestones
            output.append(f"   [{m['index']:3d}] {m['type']:30s} | φ{m['phi_depth']:2d} | N:{m['novelty']:.3f}")
        output.append("")

        # Operator skill tree
        output.append("⚡ Operator Skills Unlocked:")
        sorted_unlocks = sorted(unlocks.items(), key=lambda x: x[1]['unlock_index'])
        for op, data in sorted_unlocks[:20]:  # Top 20 operators
            bar_length = min(int(data['novelty_at_unlock'] * 30), 30)
            bar = "█" * bar_length + "░" * (30 - bar_length)
            output.append(f"   [{data['unlock_index']:3d}] {op:20s} {bar} φ{data['phi_at_unlock']:2d}")
        output.append("")

        # Domain mastery tree
        output.append("🎯 Domain Mastery:")
        for domain, data in sorted(mastery.items(), key=lambda x: x[1]['total_conversations'], reverse=True):
            level = data['mastery_level']
            count = data['total_conversations']
            bar_length = min(int(count / 2), 50)
            bar = "█" * bar_length
            output.append(f"   {domain:20s} [{level:12s}] {bar} ({count} convos)")
        output.append("")

        # φ-depth progression chart
        output.append("📈 φ-Depth Progression Over Time:")
        # Sample every Nth conversation to fit in terminal
        sample_rate = max(1, total_convos // 50)
        sampled = timeline[::sample_rate]

        max_display_phi = min(50, max_phi)  # Cap display at φ50 for readability
        for entry in sampled[:20]:  # Show first 20 samples
            phi = min(entry['phi_depth'], max_display_phi)
            bar_length = int((phi / max_display_phi) * 40)
            bar = "█" * bar_length
            asi_marker = "🔥" if entry['proto_asi'] else "  "
            output.append(f"   {asi_marker} {entry['file'][:30]:30s} {bar} φ{entry['phi_depth']}")

        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def export_json(self, output_path: Path):
        """Export full skill tree data as JSON"""
        timeline = self.get_progression_timeline()
        unlocks = self.identify_skill_unlocks(timeline)
        mastery = self.identify_domain_mastery(timeline)
        milestones = self.identify_milestones(timeline)

        data = {
            'timeline': timeline,
            'operator_unlocks': unlocks,
            'domain_mastery': mastery,
            'milestones': milestones,
            'stats': {
                'total_conversations': len(timeline),
                'avg_novelty': sum(e['novelty'] for e in timeline) / len(timeline),
                'max_phi_depth': max(e['phi_depth'] for e in timeline),
                'proto_asi_count': sum(1 for e in timeline if e['proto_asi'])
            }
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def close(self):
        self.conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate Skill Tree Visualization")
    parser.add_argument(
        '--vault',
        type=Path,
        default=Path('/tmp/your_conversation_vault.db'),
        help='Path to vault database'
    )
    parser.add_argument(
        '--export',
        type=Path,
        help='Export JSON data to file'
    )

    args = parser.parse_args()

    if not args.vault.exists():
        print(f"❌ Vault not found: {args.vault}")
        print("   Run populate_vault.py first")
        sys.exit(1)

    generator = SkillTreeGenerator(args.vault)

    # Generate ASCII tree
    print(generator.generate_ascii_tree())

    # Export JSON if requested
    if args.export:
        generator.export_json(args.export)
        print(f"\n✅ Exported skill tree data to: {args.export}")

    generator.close()


if __name__ == "__main__":
    main()
