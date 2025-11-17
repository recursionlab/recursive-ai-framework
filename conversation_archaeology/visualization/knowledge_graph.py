#!/usr/bin/env python3
"""
Knowledge Graph Generator - Operator & Domain Network

Visualizes:
- Operator co-occurrence networks
- Domain relationships
- Central hubs (most connected concepts)
- Clustering by theme
"""

import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


class KnowledgeGraphGenerator:
    """Generate knowledge graph from vault data"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def get_operator_cooccurrence(self) -> Dict[Tuple[str, str], int]:
        """Get operator co-occurrence counts"""
        cursor = self.conn.cursor()

        # Get all conversations and their operators
        cursor.execute('SELECT id FROM conversations')
        conversation_ids = [row[0] for row in cursor.fetchall()]

        cooccurrence = defaultdict(int)

        for conv_id in conversation_ids:
            # Get operators for this conversation
            cursor.execute('''
                SELECT o.operator FROM operators o
                JOIN conversation_operators co ON o.id = co.operator_id
                WHERE co.conversation_id = ?
            ''', (conv_id,))

            operators = [row[0] for row in cursor.fetchall()]

            # Count co-occurrences
            for i, op1 in enumerate(operators):
                for op2 in operators[i+1:]:
                    pair = tuple(sorted([op1, op2]))
                    cooccurrence[pair] += 1

        return dict(cooccurrence)

    def get_domain_cooccurrence(self) -> Dict[Tuple[str, str], int]:
        """Get domain co-occurrence counts"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT id FROM conversations')
        conversation_ids = [row[0] for row in cursor.fetchall()]

        cooccurrence = defaultdict(int)

        for conv_id in conversation_ids:
            cursor.execute('''
                SELECT d.domain FROM domains d
                JOIN conversation_domains cd ON d.id = cd.domain_id
                WHERE cd.conversation_id = ?
            ''', (conv_id,))

            domains = [row[0] for row in cursor.fetchall()]

            for i, d1 in enumerate(domains):
                for d2 in domains[i+1:]:
                    pair = tuple(sorted([d1, d2]))
                    cooccurrence[pair] += 1

        return dict(cooccurrence)

    def get_operator_domain_links(self) -> Dict[Tuple[str, str], int]:
        """Get operator-domain co-occurrence"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT id FROM conversations')
        conversation_ids = [row[0] for row in cursor.fetchall()]

        links = defaultdict(int)

        for conv_id in conversation_ids:
            cursor.execute('''
                SELECT o.operator FROM operators o
                JOIN conversation_operators co ON o.id = co.operator_id
                WHERE co.conversation_id = ?
            ''', (conv_id,))
            operators = [row[0] for row in cursor.fetchall()]

            cursor.execute('''
                SELECT d.domain FROM domains d
                JOIN conversation_domains cd ON d.id = cd.domain_id
                WHERE cd.conversation_id = ?
            ''', (conv_id,))
            domains = [row[0] for row in cursor.fetchall()]

            for op in operators:
                for dom in domains:
                    links[(op, dom)] += 1

        return dict(links)

    def calculate_centrality(self, edges: Dict[Tuple[str, str], int]) -> Dict[str, int]:
        """Calculate node centrality (degree)"""
        centrality = defaultdict(int)

        for (node1, node2), weight in edges.items():
            centrality[node1] += weight
            centrality[node2] += weight

        return dict(centrality)

    def generate_graphviz_dot(self, output_path: Path, min_cooccurrence: int = 2):
        """Generate Graphviz DOT format graph"""
        op_cooc = self.get_operator_cooccurrence()
        dom_cooc = self.get_domain_cooccurrence()
        op_dom_links = self.get_operator_domain_links()

        # Filter weak edges
        op_cooc = {k: v for k, v in op_cooc.items() if v >= min_cooccurrence}
        dom_cooc = {k: v for k, v in dom_cooc.items() if v >= min_cooccurrence}
        op_dom_links = {k: v for k, v in op_dom_links.items() if v >= min_cooccurrence}

        # Calculate centrality
        op_centrality = self.calculate_centrality(op_cooc)
        dom_centrality = self.calculate_centrality(dom_cooc)

        lines = []
        lines.append('digraph KnowledgeGraph {')
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box, style=rounded];')
        lines.append('')

        # Operator nodes
        lines.append('  // Operator nodes')
        lines.append('  subgraph cluster_operators {')
        lines.append('    label="Operators";')
        lines.append('    style=filled;')
        lines.append('    color=lightblue;')
        for op, centrality in sorted(op_centrality.items(), key=lambda x: x[1], reverse=True)[:30]:
            size = min(1.0 + centrality / 20.0, 3.0)
            lines.append(f'    "op_{op}" [label="{op}", fontsize={10+centrality}, width={size}];')
        lines.append('  }')
        lines.append('')

        # Domain nodes
        lines.append('  // Domain nodes')
        lines.append('  subgraph cluster_domains {')
        lines.append('    label="Domains";')
        lines.append('    style=filled;')
        lines.append('    color=lightgreen;')
        for dom, centrality in sorted(dom_centrality.items(), key=lambda x: x[1], reverse=True)[:20]:
            size = min(1.0 + centrality / 50.0, 3.0)
            lines.append(f'    "dom_{dom}" [label="{dom}", fontsize={12+centrality//10}, width={size}];')
        lines.append('  }')
        lines.append('')

        # Operator-operator edges
        lines.append('  // Operator co-occurrence')
        for (op1, op2), weight in sorted(op_cooc.items(), key=lambda x: x[1], reverse=True)[:100]:
            penwidth = min(1.0 + weight / 5.0, 5.0)
            lines.append(f'  "op_{op1}" -> "op_{op2}" [dir=none, penwidth={penwidth}, label="{weight}"];')
        lines.append('')

        # Domain-domain edges
        lines.append('  // Domain co-occurrence')
        for (d1, d2), weight in sorted(dom_cooc.items(), key=lambda x: x[1], reverse=True)[:50]:
            penwidth = min(1.0 + weight / 10.0, 5.0)
            lines.append(f'  "dom_{d1}" -> "dom_{d2}" [dir=none, penwidth={penwidth}, label="{weight}", color=green];')
        lines.append('')

        # Operator-domain edges
        lines.append('  // Operator-domain links')
        for (op, dom), weight in sorted(op_dom_links.items(), key=lambda x: x[1], reverse=True)[:200]:
            penwidth = min(0.5 + weight / 10.0, 3.0)
            lines.append(f'  "op_{op}" -> "dom_{dom}" [penwidth={penwidth}, style=dashed, color=gray];')

        lines.append('}')

        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))

    def generate_network_stats(self) -> str:
        """Generate network statistics report"""
        op_cooc = self.get_operator_cooccurrence()
        dom_cooc = self.get_domain_cooccurrence()
        op_dom_links = self.get_operator_domain_links()

        op_centrality = self.calculate_centrality(op_cooc)
        dom_centrality = self.calculate_centrality(dom_cooc)

        output = []
        output.append("=" * 80)
        output.append("📊 KNOWLEDGE GRAPH STATISTICS")
        output.append("=" * 80)
        output.append("")

        # Overall stats
        output.append(f"Network Overview:")
        output.append(f"  Operator nodes: {len(op_centrality)}")
        output.append(f"  Domain nodes: {len(dom_centrality)}")
        output.append(f"  Operator-operator edges: {len(op_cooc)}")
        output.append(f"  Domain-domain edges: {len(dom_cooc)}")
        output.append(f"  Operator-domain edges: {len(op_dom_links)}")
        output.append("")

        # Most central operators
        output.append("🔥 Most Central Operators (Hub Concepts):")
        for op, centrality in sorted(op_centrality.items(), key=lambda x: x[1], reverse=True)[:20]:
            bar = "█" * min(centrality // 5, 40)
            output.append(f"  {op:20s} {bar} ({centrality} connections)")
        output.append("")

        # Most central domains
        output.append("🎯 Most Central Domains:")
        for dom, centrality in sorted(dom_centrality.items(), key=lambda x: x[1], reverse=True)[:15]:
            bar = "█" * min(centrality // 10, 40)
            output.append(f"  {dom:20s} {bar} ({centrality} connections)")
        output.append("")

        # Strongest operator pairs
        output.append("⚡ Strongest Operator Pairs (Co-occurrence):")
        for (op1, op2), weight in sorted(op_cooc.items(), key=lambda x: x[1], reverse=True)[:15]:
            output.append(f"  {op1:15s} ↔ {op2:15s}  ({weight} times)")
        output.append("")

        # Strongest domain pairs
        output.append("🔗 Strongest Domain Pairs:")
        for (d1, d2), weight in sorted(dom_cooc.items(), key=lambda x: x[1], reverse=True)[:10]:
            output.append(f"  {d1:20s} ↔ {d2:20s}  ({weight} times)")
        output.append("")

        # Top operator-domain associations
        output.append("🎯 Top Operator-Domain Associations:")
        for (op, dom), weight in sorted(op_dom_links.items(), key=lambda x: x[1], reverse=True)[:20]:
            output.append(f"  {op:20s} → {dom:20s}  ({weight} times)")

        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def export_json(self, output_path: Path):
        """Export graph data as JSON"""
        data = {
            'operator_cooccurrence': {f"{k[0]}_{k[1]}": v for k, v in self.get_operator_cooccurrence().items()},
            'domain_cooccurrence': {f"{k[0]}_{k[1]}": v for k, v in self.get_domain_cooccurrence().items()},
            'operator_domain_links': {f"{k[0]}_{k[1]}": v for k, v in self.get_operator_domain_links().items()},
            'operator_centrality': self.calculate_centrality(self.get_operator_cooccurrence()),
            'domain_centrality': self.calculate_centrality(self.get_domain_cooccurrence())
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def close(self):
        self.conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate Knowledge Graph")
    parser.add_argument(
        '--vault',
        type=Path,
        default=Path('/tmp/your_conversation_vault.db'),
        help='Path to vault database'
    )
    parser.add_argument(
        '--dot',
        type=Path,
        help='Export Graphviz DOT file'
    )
    parser.add_argument(
        '--json',
        type=Path,
        help='Export JSON data'
    )
    parser.add_argument(
        '--min-cooccurrence',
        type=int,
        default=2,
        help='Minimum co-occurrence count for edges'
    )

    args = parser.parse_args()

    if not args.vault.exists():
        print(f"❌ Vault not found: {args.vault}")
        print("   Run populate_vault.py first")
        sys.exit(1)

    generator = KnowledgeGraphGenerator(args.vault)

    # Generate stats
    print(generator.generate_network_stats())

    # Export DOT if requested
    if args.dot:
        generator.generate_graphviz_dot(args.dot, args.min_cooccurrence)
        print(f"\n✅ Exported Graphviz DOT to: {args.dot}")
        print(f"   Generate PNG: dot -Tpng {args.dot} -o graph.png")

    # Export JSON if requested
    if args.json:
        generator.export_json(args.json)
        print(f"\n✅ Exported JSON data to: {args.json}")

    generator.close()


if __name__ == "__main__":
    main()
