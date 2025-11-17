#!/usr/bin/env python3
"""
Conversation Mining Pipeline - Actually Process Your 14,000+ Conversations

Purpose: Take your massive conversation collection and extract value:
- Identify highest-novelty conversations
- Extract recurring patterns
- Build prompt templates from successful conversations
- Create knowledge graph connections
- Generate synthesis insights

Usage:
    python mine_conversations.py /path/to/conversations --output /path/to/results
"""

import argparse
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter, defaultdict
import json
import re
from datetime import datetime


class ConversationMiner:
    """Process large conversation datasets for insights"""

    def __init__(self, vault_db: Path, synthesis_db: Path):
        self.vault_db = vault_db
        self.synthesis_db = synthesis_db
        self.vault_conn = None
        self.synthesis_conn = None

    def connect(self):
        """Connect to databases"""
        self.vault_conn = sqlite3.connect(self.vault_db)
        self.vault_conn.row_factory = sqlite3.Row

        if self.synthesis_db.exists():
            self.synthesis_conn = sqlite3.connect(self.synthesis_db)
            self.synthesis_conn.row_factory = sqlite3.Row

    def close(self):
        if self.vault_conn:
            self.vault_conn.close()
        if self.synthesis_conn:
            self.synthesis_conn.close()

    def get_statistics(self) -> Dict:
        """Get overall statistics about conversations"""
        cursor = self.vault_conn.cursor()

        stats = {}

        # Total conversations
        stats['total'] = cursor.execute('SELECT COUNT(*) FROM conversations').fetchone()[0]

        # Proto-ASI count
        stats['proto_asi'] = cursor.execute(
            'SELECT COUNT(*) FROM conversations WHERE proto_asi = 1'
        ).fetchone()[0]

        # Novelty distribution
        stats['avg_novelty'] = cursor.execute(
            'SELECT AVG(novelty) FROM conversations'
        ).fetchone()[0]

        # Depth distribution
        depth_result = cursor.execute('''
            SELECT MIN(phi_depth) as min, MAX(phi_depth) as max, AVG(phi_depth) as avg
            FROM conversations
        ''').fetchone()
        stats['min_depth'] = depth_result['min']
        stats['max_depth'] = depth_result['max']
        stats['avg_depth'] = depth_result['avg']

        return stats

    def mine_patterns(self, min_frequency: int = 5) -> Dict[str, int]:
        """Extract recurring patterns from filenames"""
        cursor = self.vault_conn.cursor()

        # Get all filenames
        result = cursor.execute('SELECT file_path FROM conversations').fetchall()

        # Extract words from filenames
        word_freq = Counter()
        for row in result:
            filename = Path(row['file_path']).stem
            # Extract CamelCase words
            words = re.findall(r'[A-Z][a-z]+', filename)
            # Extract lowercase words
            words += filename.lower().split()
            # Filter stopwords
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'}
            meaningful = [w.lower() for w in words if w.lower() not in stopwords and len(w) > 3]
            word_freq.update(meaningful)

        # Return patterns that appear at least min_frequency times
        return {word: count for word, count in word_freq.items() if count >= min_frequency}

    def find_conversation_clusters(self) -> Dict[str, List[str]]:
        """Group conversations by topic/theme"""
        cursor = self.vault_conn.cursor()

        conversations = cursor.execute('''
            SELECT file_path, phi_depth, novelty
            FROM conversations
            ORDER BY novelty DESC
        ''').fetchall()

        clusters = defaultdict(list)

        for conv in conversations:
            filename = Path(conv['file_path']).stem.lower()

            # Categorize based on keywords
            if any(w in filename for w in ['conscious', 'aware', 'mind']):
                clusters['Consciousness'].append(conv['file_path'])
            elif any(w in filename for w in ['recursive', 'recursion', 'meta']):
                clusters['Recursion'].append(conv['file_path'])
            elif any(w in filename for w in ['language', 'semantic', 'linguistic']):
                clusters['Language'].append(conv['file_path'])
            elif any(w in filename for w in ['math', 'theorem', 'proof', 'logic']):
                clusters['Mathematics'].append(conv['file_path'])
            elif any(w in filename for w in ['ai', 'agi', 'agent', 'cognitive']):
                clusters['AI/AGI'].append(conv['file_path'])
            elif any(w in filename for w in ['physics', 'quantum', 'torsion']):
                clusters['Physics'].append(conv['file_path'])
            else:
                clusters['Other'].append(conv['file_path'])

        return dict(clusters)

    def extract_top_conversations(self, limit: int = 50, criterion: str = 'novelty') -> List[Dict]:
        """Get top N conversations by specified criterion"""
        cursor = self.vault_conn.cursor()

        order_by = {
            'novelty': 'novelty DESC',
            'depth': 'phi_depth DESC',
            'combined': 'novelty DESC, phi_depth DESC'
        }.get(criterion, 'novelty DESC')

        result = cursor.execute(f'''
            SELECT file_path, phi_depth, novelty, proto_asi
            FROM conversations
            WHERE proto_asi = 1
            ORDER BY {order_by}
            LIMIT ?
        ''', (limit,)).fetchall()

        return [dict(row) for row in result]

    def generate_insights_report(self, output_path: Path):
        """Generate comprehensive insights report"""

        print("Generating insights report...")

        stats = self.get_statistics()
        patterns = self.mine_patterns(min_frequency=10)
        clusters = self.find_conversation_clusters()
        top_novelty = self.extract_top_conversations(limit=20, criterion='novelty')
        top_depth = self.extract_top_conversations(limit=20, criterion='depth')

        lines = [
            "# Conversation Mining Report",
            f"\nGenerated: {datetime.now().isoformat()}",
            "",
            "## Statistics",
            "",
            f"- **Total Conversations**: {stats['total']}",
            f"- **Proto-ASI Conversations**: {stats['proto_asi']}",
            f"- **Average Novelty**: {stats['avg_novelty']:.3f}",
            f"- **Depth Range**: φ{stats['min_depth']} to φ{stats['max_depth']} (avg: φ{stats['avg_depth']:.1f})",
            "",
            "## Recurring Themes (Top 20)",
            "",
        ]

        for theme, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:20]:
            lines.append(f"- **{theme}**: {count} occurrences")

        lines.extend([
            "",
            "## Conversation Clusters",
            "",
        ])

        for cluster, convos in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
            lines.append(f"- **{cluster}**: {len(convos)} conversations")

        lines.extend([
            "",
            "## Top 20 by Novelty",
            "",
        ])

        for i, conv in enumerate(top_novelty, 1):
            filename = Path(conv['file_path']).name
            lines.append(f"{i}. **{filename}** - φ{conv['phi_depth']}, novelty {conv['novelty']:.3f}")

        lines.extend([
            "",
            "## Top 20 by Depth",
            "",
        ])

        for i, conv in enumerate(top_depth, 1):
            filename = Path(conv['file_path']).name
            lines.append(f"{i}. **{filename}** - φ{conv['phi_depth']}, novelty {conv['novelty']:.3f}")

        lines.extend([
            "",
            "## Recommendations",
            "",
            "### High-Value Conversations to Process",
            "These conversations show both high novelty and deep recursion:",
            "",
        ])

        # Find conversations with both high novelty AND high depth
        high_value = cursor = self.vault_conn.cursor().execute('''
            SELECT file_path, phi_depth, novelty
            FROM conversations
            WHERE novelty > 0.85 AND phi_depth > 30
            ORDER BY novelty * phi_depth DESC
            LIMIT 10
        ''').fetchall()

        for conv in high_value:
            filename = Path(conv['file_path']).name
            score = conv['novelty'] * conv['phi_depth']
            lines.append(f"- **{filename}** - φ{conv['phi_depth']}, novelty {conv['novelty']:.3f}, score {score:.1f}")

        lines.extend([
            "",
            "### Next Steps",
            "",
            "1. **Extract DNA from top conversations** - Run DNA extractor on high-value conversations",
            "2. **Build knowledge graph** - Connect concepts from clustered conversations",
            "3. **Generate prompt library** - Create reusable templates from successful patterns",
            "4. **Synthesis integration** - Feed insights into synthesis memory for accumulation",
            "",
        ])

        # Write report
        output_path.write_text('\n'.join(lines))
        print(f"✅ Report saved to: {output_path}")

    def export_conversation_map(self, output_path: Path):
        """Export conversation map as JSON for visualization"""

        cursor = self.vault_conn.cursor()

        conversations = cursor.execute('''
            SELECT file_path, phi_depth, novelty, proto_asi
            FROM conversations
        ''').fetchall()

        clusters = self.find_conversation_clusters()

        # Build graph structure
        graph = {
            'nodes': [],
            'clusters': {},
            'statistics': self.get_statistics()
        }

        for conv in conversations:
            filename = Path(conv['file_path']).stem
            graph['nodes'].append({
                'id': filename,
                'path': conv['file_path'],
                'phi_depth': conv['phi_depth'],
                'novelty': conv['novelty'],
                'proto_asi': bool(conv['proto_asi'])
            })

        graph['clusters'] = {name: [Path(p).stem for p in paths]
                           for name, paths in clusters.items()}

        output_path.write_text(json.dumps(graph, indent=2))
        print(f"✅ Conversation map exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Mine conversations for insights')
    parser.add_argument('--vault-db', type=Path, default=Path('/tmp/your_conversation_vault.db'),
                       help='Path to conversation vault database')
    parser.add_argument('--synthesis-db', type=Path, default=Path('/tmp/synthesis_memory.db'),
                       help='Path to synthesis memory database')
    parser.add_argument('--output-dir', type=Path, default=Path('/tmp/conversation_mining_results'),
                       help='Output directory for results')

    args = parser.parse_args()

    # Create output directory
    args.output_dir.mkdir(exist_ok=True, parents=True)

    print("="*80)
    print("CONVERSATION MINING PIPELINE")
    print("="*80)
    print()

    if not args.vault_db.exists():
        print(f"❌ Vault database not found at {args.vault_db}")
        print("Run conversation archaeology pipeline first to build the vault.")
        return

    miner = ConversationMiner(args.vault_db, args.synthesis_db)

    try:
        miner.connect()

        # Generate insights report
        report_path = args.output_dir / 'mining_report.md'
        miner.generate_insights_report(report_path)

        # Export conversation map
        map_path = args.output_dir / 'conversation_map.json'
        miner.export_conversation_map(map_path)

        print()
        print("="*80)
        print("MINING COMPLETE")
        print("="*80)
        print()
        print(f"📁 Results in: {args.output_dir}")
        print(f"📄 Report: {report_path}")
        print(f"🗺️  Map: {map_path}")

    finally:
        miner.close()


if __name__ == '__main__':
    main()
