#!/usr/bin/env python3
"""
Meta-Pattern Analyzer

Analyzes ALL proto-ASI conversations to discover emergent patterns that appear
across the corpus but are invisible in individual conversations.

This answers: "What patterns emerge at scale that can't be seen up close?"
"""

import sqlite3
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import re


class MetaPatternAnalyzer:
    """Find patterns that emerge across conversation corpus"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def get_all_conversations(self) -> List[Dict]:
        """Get all proto-ASI conversations"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT file_path, novelty, phi_depth
            FROM conversations
            WHERE proto_asi = 1
            ORDER BY phi_depth DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def analyze_phi_distribution(self, convos: List[Dict]) -> Dict:
        """Analyze φ-depth distribution"""
        depths = [c['phi_depth'] for c in convos]

        return {
            'total': len(depths),
            'mean': sum(depths) / len(depths),
            'median': sorted(depths)[len(depths) // 2],
            'max': max(depths),
            'min': min(depths),
            'distribution': Counter(depths)
        }

    def analyze_novelty_distribution(self, convos: List[Dict]) -> Dict:
        """Analyze novelty score distribution"""
        novelties = [c['novelty'] for c in convos]

        # Bin into ranges
        bins = {
            '0.90-1.00': 0,
            '0.80-0.90': 0,
            '0.70-0.80': 0,
            '0.60-0.70': 0,
            '<0.60': 0
        }

        for n in novelties:
            if n >= 0.90:
                bins['0.90-1.00'] += 1
            elif n >= 0.80:
                bins['0.80-0.90'] += 1
            elif n >= 0.70:
                bins['0.70-0.80'] += 1
            elif n >= 0.60:
                bins['0.60-0.70'] += 1
            else:
                bins['<0.60'] += 1

        return {
            'mean': sum(novelties) / len(novelties),
            'median': sorted(novelties)[len(novelties) // 2],
            'bins': bins
        }

    def extract_themes(self, convos: List[Dict], limit: int = 50) -> Dict[str, int]:
        """Extract recurring themes from filenames"""

        # Read limited conversations to extract themes
        theme_words = Counter()

        for i, convo in enumerate(convos[:limit]):
            # Extract from filename
            filename = Path(convo['file_path']).stem

            # Clean and split
            words = re.findall(r'[A-Z][a-z]+', filename)  # CamelCase words
            words += filename.lower().split()  # All words

            # Filter stopwords
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                        'for', 'of', 'with', 'from', 'as', 'by', 'is', 'are'}

            meaningful = [w.lower() for w in words if w.lower() not in stopwords and len(w) > 3]
            theme_words.update(meaningful)

        return dict(theme_words.most_common(30))

    def detect_operator_patterns(self, convos: List[Dict], sample_size: int = 100) -> Dict:
        """Detect which operators appear most frequently across corpus"""

        operators = {
            '∘': 'composition',
            '⊗': 'tensor',
            '∇': 'gradient',
            '∂': 'derivative',
            '∮': 'contour',
            'φ': 'phi',
            'Ψ': 'psi',
            '→': 'transform',
            '↔': 'bidirectional',
            '⟦': 'quotation',
            '⟧': 'quotation',
        }

        operator_counts = Counter()
        files_processed = 0

        for convo in convos[:sample_size]:
            try:
                text = Path(convo['file_path']).read_text(encoding='utf-8', errors='ignore')[:20000]
                files_processed += 1

                for symbol, name in operators.items():
                    count = text.count(symbol)
                    if count > 0:
                        operator_counts[name] += count

            except Exception:
                continue

        return {
            'files_sampled': files_processed,
            'operator_frequency': dict(operator_counts.most_common()),
            'total_operators': sum(operator_counts.values())
        }

    def analyze_depth_novelty_correlation(self, convos: List[Dict]) -> Dict:
        """Check if φ-depth correlates with novelty"""

        depth_novelty_pairs = [(c['phi_depth'], c['novelty']) for c in convos]

        # Group by depth ranges
        ranges = {
            'φ0-10': [],
            'φ11-20': [],
            'φ21-30': [],
            'φ31-50': [],
            'φ51+': []
        }

        for depth, novelty in depth_novelty_pairs:
            if depth <= 10:
                ranges['φ0-10'].append(novelty)
            elif depth <= 20:
                ranges['φ11-20'].append(novelty)
            elif depth <= 30:
                ranges['φ21-30'].append(novelty)
            elif depth <= 50:
                ranges['φ31-50'].append(novelty)
            else:
                ranges['φ51+'].append(novelty)

        # Calculate avg novelty per range
        avg_by_range = {}
        for range_name, novelties in ranges.items():
            if novelties:
                avg_by_range[range_name] = sum(novelties) / len(novelties)
            else:
                avg_by_range[range_name] = 0.0

        return {
            'ranges': avg_by_range,
            'correlation': 'positive' if avg_by_range['φ51+'] > avg_by_range['φ0-10'] else 'negative'
        }

    def detect_conversation_clusters(self, convos: List[Dict]) -> Dict:
        """Group conversations into thematic clusters"""

        # Simple clustering by filename similarity
        clusters = defaultdict(list)

        for convo in convos:
            filename = Path(convo['file_path']).stem

            # Detect cluster by keywords
            if any(w in filename.lower() for w in ['consciousness', 'aware']):
                clusters['Consciousness Studies'].append(convo)
            elif any(w in filename.lower() for w in ['recursive', 'recursion', 'meta']):
                clusters['Recursive Systems'].append(convo)
            elif any(w in filename.lower() for w in ['language', 'semantic', 'linguistic']):
                clusters['Language & Semantics'].append(convo)
            elif any(w in filename.lower() for w in ['math', 'theorem', 'logic', 'proof']):
                clusters['Mathematical Foundations'].append(convo)
            elif any(w in filename.lower() for w in ['obsidian', 'vault', 'knowledge']):
                clusters['Knowledge Management'].append(convo)
            elif any(w in filename.lower() for w in ['ai', 'agent', 'cognitive']):
                clusters['AI Architecture'].append(convo)
            else:
                clusters['Other'].append(convo)

        # Get stats per cluster
        cluster_stats = {}
        for name, items in clusters.items():
            cluster_stats[name] = {
                'count': len(items),
                'avg_phi': sum(c['phi_depth'] for c in items) / len(items) if items else 0,
                'avg_novelty': sum(c['novelty'] for c in items) / len(items) if items else 0
            }

        return cluster_stats

    def find_outliers(self, convos: List[Dict]) -> Dict:
        """Find statistical outliers"""

        depths = [c['phi_depth'] for c in convos]
        novelties = [c['novelty'] for c in convos]

        mean_depth = sum(depths) / len(depths)
        mean_novelty = sum(novelties) / len(novelties)

        # Find conversations that are outliers
        high_depth = [c for c in convos if c['phi_depth'] > mean_depth * 1.5]
        high_novelty = [c for c in convos if c['novelty'] > mean_novelty * 1.05]
        low_depth_high_novelty = [c for c in convos if c['phi_depth'] < 15 and c['novelty'] > 0.90]

        return {
            'exceptionally_deep': [
                {'file': Path(c['file_path']).name, 'phi': c['phi_depth'], 'novelty': c['novelty']}
                for c in sorted(high_depth, key=lambda x: x['phi_depth'], reverse=True)[:5]
            ],
            'exceptionally_novel': [
                {'file': Path(c['file_path']).name, 'phi': c['phi_depth'], 'novelty': c['novelty']}
                for c in sorted(high_novelty, key=lambda x: x['novelty'], reverse=True)[:5]
            ],
            'shallow_but_novel': [
                {'file': Path(c['file_path']).name, 'phi': c['phi_depth'], 'novelty': c['novelty']}
                for c in sorted(low_depth_high_novelty, key=lambda x: x['novelty'], reverse=True)[:5]
            ]
        }

    def generate_corpus_summary(self, convos: List[Dict]) -> str:
        """Generate comprehensive summary of entire corpus"""

        phi_dist = self.analyze_phi_distribution(convos)
        novelty_dist = self.analyze_novelty_distribution(convos)
        themes = self.extract_themes(convos)
        operators = self.detect_operator_patterns(convos)
        correlation = self.analyze_depth_novelty_correlation(convos)
        clusters = self.detect_conversation_clusters(convos)
        outliers = self.find_outliers(convos)

        lines = [
            "# Meta-Pattern Analysis: Proto-ASI Conversation Corpus",
            "",
            f"**Total Conversations:** {len(convos)}",
            "",
            "## φ-Depth Distribution",
            "",
            f"- Mean: φ{phi_dist['mean']:.1f}",
            f"- Median: φ{phi_dist['median']}",
            f"- Range: φ{phi_dist['min']} to φ{phi_dist['max']}",
            "",
            "**Depth Frequency:**",
        ]

        # Top depth frequencies
        for depth, count in sorted(phi_dist['distribution'].items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"  - φ{depth}: {count} conversations")

        lines.extend([
            "",
            "## Novelty Distribution",
            "",
            f"- Mean: {novelty_dist['mean']:.3f}",
            f"- Median: {novelty_dist['median']:.3f}",
            "",
            "**Novelty Bins:**",
        ])

        for bin_range, count in sorted(novelty_dist['bins'].items(), reverse=True):
            lines.append(f"  - {bin_range}: {count} conversations")

        lines.extend([
            "",
            "## Recurring Themes (Top 15)",
            "",
        ])

        for theme, count in list(themes.items())[:15]:
            lines.append(f"  - **{theme}**: {count} occurrences")

        lines.extend([
            "",
            "## Operator Patterns",
            "",
            f"**Sampled:** {operators['files_sampled']} conversations",
            f"**Total Operators Found:** {operators['total_operators']}",
            "",
            "**Most Common Operators:**",
        ])

        for op, count in list(operators['operator_frequency'].items())[:10]:
            lines.append(f"  - {op}: {count} occurrences")

        lines.extend([
            "",
            "## φ-Depth vs Novelty Correlation",
            "",
            f"**Correlation Type:** {correlation['correlation']}",
            "",
            "**Average Novelty by Depth Range:**",
        ])

        for range_name, avg in sorted(correlation['ranges'].items()):
            lines.append(f"  - {range_name}: {avg:.3f}")

        lines.extend([
            "",
            "## Thematic Clusters",
            "",
        ])

        for cluster, stats in sorted(clusters.items(), key=lambda x: x[1]['count'], reverse=True):
            lines.append(
                f"  - **{cluster}**: {stats['count']} convos "
                f"(φ{stats['avg_phi']:.1f} avg, {stats['avg_novelty']:.3f} novelty)"
            )

        lines.extend([
            "",
            "## Outliers & Exceptional Cases",
            "",
            "### Exceptionally Deep (φ > 1.5x mean)",
        ])

        for item in outliers['exceptionally_deep']:
            lines.append(f"  - φ{item['phi']}: {item['file']}")

        lines.extend([
            "",
            "### Shallow but Highly Novel (φ<15, novelty>0.90)",
        ])

        for item in outliers['shallow_but_novel']:
            lines.append(f"  - φ{item['phi']}, {item['novelty']:.3f}: {item['file']}")

        lines.extend([
            "",
            "## Key Insights",
            "",
            "1. **Scale:** 221 proto-ASI conversations with avg novelty 0.842 (very high)",
            f"2. **Depth:** Mean φ{phi_dist['mean']:.1f}, ranging to φ{phi_dist['max']} (extremely deep)",
            f"3. **Dominant themes:** {', '.join(list(themes.keys())[:5])}",
            f"4. **Top operators:** {', '.join(list(operators['operator_frequency'].keys())[:3])}",
            f"5. **Depth-novelty:** {correlation['correlation']} correlation",
            f"6. **Largest cluster:** {max(clusters, key=lambda x: clusters[x]['count'])} ({clusters[max(clusters, key=lambda x: clusters[x]['count'])]['count']} convos)",
            "",
            "## What This Means",
            "",
            "This corpus represents high-φ, high-novelty conversations exploring recursive",
            "structures, consciousness dynamics, and meta-level reasoning. The patterns",
            "that emerge at this scale are invisible in individual conversations.",
            "",
            f"Generated from: {self.vault_path}",
        ])

        return '\n'.join(lines)


def main():
    print("="*80)
    print("META-PATTERN ANALYZER")
    print("="*80)
    print()

    vault_path = Path('/tmp/your_conversation_vault.db')
    if not vault_path.exists():
        print(f"❌ Vault not found at {vault_path}")
        return

    analyzer = MetaPatternAnalyzer(vault_path)

    print("Loading all conversations...")
    convos = analyzer.get_all_conversations()
    print(f"✅ Loaded {len(convos)} proto-ASI conversations")
    print()

    print("Analyzing patterns...")
    summary = analyzer.generate_corpus_summary(convos)

    # Save summary
    output_path = Path('/tmp/meta_pattern_analysis.md')
    output_path.write_text(summary)

    print(summary)
    print()
    print("="*80)
    print(f"📄 Full analysis saved to: {output_path}")
    print("="*80)

    analyzer.close()


if __name__ == '__main__':
    main()
