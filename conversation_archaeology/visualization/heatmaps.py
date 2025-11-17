#!/usr/bin/env python3
"""
Heatmap Generators - Temporal and Distribution Views

Visualizes:
- φ-depth progression over time
- Novelty distribution heatmap
- Domain activity over time
- Operator usage patterns
"""

import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


class HeatmapGenerator:
    """Generate heatmap visualizations from vault data"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def get_timeline_data(self) -> List[Dict]:
        """Get chronological conversation data"""
        cursor = self.conn.cursor()

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
            # Get domains for this conversation
            cursor.execute('''
                SELECT d.domain FROM domains d
                JOIN conversation_domains cd ON d.id = cd.domain_id
                JOIN conversations c ON cd.conversation_id = c.id
                WHERE c.file_path = ?
            ''', (row['file_path'],))
            domains = [r[0] for r in cursor.fetchall()]

            # Get operators
            cursor.execute('''
                SELECT o.operator FROM operators o
                JOIN conversation_operators co ON o.id = co.operator_id
                JOIN conversations c ON co.conversation_id = c.id
                WHERE c.file_path = ?
            ''', (row['file_path'],))
            operators = [r[0] for r in cursor.fetchall()]

            timeline.append({
                'file': Path(row['file_path']).name,
                'novelty': row['novelty'],
                'phi_depth': row['phi_depth'],
                'proto_asi': bool(row['proto_asi']),
                'domains': domains,
                'operators': operators
            })

        return timeline

    def generate_phi_depth_ascii_heatmap(self, width: int = 80, height: int = 30) -> str:
        """Generate ASCII heatmap of φ-depth over time"""
        timeline = self.get_timeline_data()
        total = len(timeline)

        if total == 0:
            return "No data"

        output = []
        output.append("=" * width)
        output.append("φ-DEPTH PROGRESSION HEATMAP".center(width))
        output.append("=" * width)
        output.append("")

        # Determine max phi for scaling
        max_phi = max(e['phi_depth'] for e in timeline)
        max_phi_display = min(max_phi, 100)  # Cap display

        # Create buckets for timeline
        bucket_size = max(1, total // width)
        buckets = []
        for i in range(0, total, bucket_size):
            bucket = timeline[i:i+bucket_size]
            avg_phi = sum(e['phi_depth'] for e in bucket) / len(bucket)
            max_phi_bucket = max(e['phi_depth'] for e in bucket)
            asi_ratio = sum(1 for e in bucket if e['proto_asi']) / len(bucket)
            buckets.append({
                'avg_phi': avg_phi,
                'max_phi': max_phi_bucket,
                'asi_ratio': asi_ratio
            })

        # Generate heatmap rows
        chars = ' ░▒▓█'
        for level in range(height, 0, -1):
            threshold = (level / height) * max_phi_display
            line = []
            for bucket in buckets:
                if bucket['avg_phi'] >= threshold:
                    # Intensity based on ASI emergence
                    intensity = min(int(bucket['asi_ratio'] * len(chars)), len(chars) - 1)
                    line.append(chars[intensity])
                else:
                    line.append(' ')

            # Add scale label
            phi_label = f"φ{int(threshold):3d}"
            output.append(f"{phi_label} │{''.join(line)}│")

        # Timeline axis
        output.append("     └" + "─" * len(buckets) + "┘")
        output.append(f"      0{' ' * (len(buckets)//2 - 6)}Timeline{' ' * (len(buckets)//2 - 4)}{total}")
        output.append("")
        output.append(f"Legend: {' ░▒▓█'} = Increasing proto-ASI density")
        output.append("")

        return "\n".join(output)

    def generate_novelty_distribution_heatmap(self) -> str:
        """Generate novelty distribution visualization"""
        timeline = self.get_timeline_data()

        output = []
        output.append("=" * 80)
        output.append("NOVELTY DISTRIBUTION HEATMAP")
        output.append("=" * 80)
        output.append("")

        # Create novelty buckets
        buckets = {
            '0.9-1.0': [],
            '0.8-0.9': [],
            '0.7-0.8': [],
            '0.6-0.7': [],
            '0.5-0.6': [],
            '< 0.5': []
        }

        for entry in timeline:
            nov = entry['novelty']
            if nov >= 0.9:
                buckets['0.9-1.0'].append(entry)
            elif nov >= 0.8:
                buckets['0.8-0.9'].append(entry)
            elif nov >= 0.7:
                buckets['0.7-0.8'].append(entry)
            elif nov >= 0.6:
                buckets['0.6-0.7'].append(entry)
            elif nov >= 0.5:
                buckets['0.5-0.6'].append(entry)
            else:
                buckets['< 0.5'].append(entry)

        # Display distribution
        max_count = max(len(entries) for entries in buckets.values())
        for bucket_name, entries in buckets.items():
            count = len(entries)
            percentage = (count / len(timeline)) * 100 if timeline else 0
            bar_length = int((count / max_count) * 60) if max_count > 0 else 0
            bar = "█" * bar_length
            asi_count = sum(1 for e in entries if e['proto_asi'])

            output.append(f"  {bucket_name:8s} │{bar:60s}│ {count:4d} ({percentage:5.1f}%) | ASI: {asi_count}")

        output.append("")
        output.append(f"Total conversations: {len(timeline)}")
        output.append(f"Average novelty: {sum(e['novelty'] for e in timeline) / len(timeline):.3f}")
        output.append("")

        return "\n".join(output)

    def generate_domain_activity_timeline(self) -> str:
        """Generate domain activity over time"""
        timeline = self.get_timeline_data()

        output = []
        output.append("=" * 80)
        output.append("DOMAIN ACTIVITY TIMELINE")
        output.append("=" * 80)
        output.append("")

        # Get all unique domains
        all_domains = set()
        for entry in timeline:
            all_domains.update(entry['domains'])

        # Track domain appearance over time
        # Split timeline into chunks
        chunk_size = max(1, len(timeline) // 40)
        chunks = []
        for i in range(0, len(timeline), chunk_size):
            chunk = timeline[i:i+chunk_size]
            domain_counts = defaultdict(int)
            for entry in chunk:
                for domain in entry['domains']:
                    domain_counts[domain] += 1
            chunks.append(domain_counts)

        # Display domain activity
        for domain in sorted(all_domains)[:15]:  # Top 15 domains
            line = [domain[:18].ljust(18), " │ "]
            for chunk_counts in chunks:
                count = chunk_counts.get(domain, 0)
                if count == 0:
                    line.append(' ')
                elif count <= 2:
                    line.append('░')
                elif count <= 5:
                    line.append('▒')
                elif count <= 10:
                    line.append('▓')
                else:
                    line.append('█')
            line.append(" │")
            output.append(''.join(line))

        output.append("   " + " " * 18 + " └" + "─" * len(chunks) + "┘")
        output.append("   " + " " * 20 + "Timeline →")
        output.append("")

        return "\n".join(output)

    def generate_operator_usage_heatmap(self) -> str:
        """Generate operator usage patterns"""
        timeline = self.get_timeline_data()

        output = []
        output.append("=" * 80)
        output.append("OPERATOR USAGE HEATMAP")
        output.append("=" * 80)
        output.append("")

        # Count operator usage
        operator_counts = defaultdict(int)
        for entry in timeline:
            for op in entry['operators']:
                operator_counts[op] += 1

        # Display top operators
        output.append("Top 30 Most Used Operators:")
        output.append("")

        max_count = max(operator_counts.values()) if operator_counts else 1
        for op, count in sorted(operator_counts.items(), key=lambda x: x[1], reverse=True)[:30]:
            bar_length = int((count / max_count) * 50)
            bar = "█" * bar_length
            percentage = (count / len(timeline)) * 100
            output.append(f"  {op:20s} │{bar:50s}│ {count:4d} ({percentage:5.1f}%)")

        output.append("")

        return "\n".join(output)

    def export_all_heatmaps(self, output_path: Path):
        """Export all heatmaps to single text file"""
        with open(output_path, 'w') as f:
            f.write(self.generate_phi_depth_ascii_heatmap())
            f.write("\n\n")
            f.write(self.generate_novelty_distribution_heatmap())
            f.write("\n\n")
            f.write(self.generate_domain_activity_timeline())
            f.write("\n\n")
            f.write(self.generate_operator_usage_heatmap())

    def close(self):
        self.conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate Heatmap Visualizations")
    parser.add_argument(
        '--vault',
        type=Path,
        default=Path('/tmp/your_conversation_vault.db'),
        help='Path to vault database'
    )
    parser.add_argument(
        '--export',
        type=Path,
        help='Export all heatmaps to text file'
    )
    parser.add_argument(
        '--type',
        choices=['phi', 'novelty', 'domains', 'operators', 'all'],
        default='all',
        help='Type of heatmap to generate'
    )

    args = parser.parse_args()

    if not args.vault.exists():
        print(f"❌ Vault not found: {args.vault}")
        print("   Run populate_vault.py first")
        sys.exit(1)

    generator = HeatmapGenerator(args.vault)

    # Generate requested heatmaps
    if args.type in ['phi', 'all']:
        print(generator.generate_phi_depth_ascii_heatmap())
        print()

    if args.type in ['novelty', 'all']:
        print(generator.generate_novelty_distribution_heatmap())
        print()

    if args.type in ['domains', 'all']:
        print(generator.generate_domain_activity_timeline())
        print()

    if args.type in ['operators', 'all']:
        print(generator.generate_operator_usage_heatmap())
        print()

    # Export if requested
    if args.export:
        generator.export_all_heatmaps(args.export)
        print(f"✅ Exported all heatmaps to: {args.export}")

    generator.close()


if __name__ == "__main__":
    main()
