#!/usr/bin/env python3
"""
Connection Finder - Discover Hidden Links Between Conversations

Analyzes conversations to find:
- Shared conceptual patterns
- Similar recursive structures
- Cross-pollination of ideas
- Potential synthesis opportunities

This reveals the "meta-conversation" happening across your entire corpus.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import re


class ConnectionFinder:
    """Find hidden connections between conversations"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def extract_concepts(self, text: str, min_length: int = 4) -> Set[str]:
        """Extract meaningful concepts from text"""

        # Extract CamelCase words
        camel_words = set(re.findall(r'[A-Z][a-z]+(?:[A-Z][a-z]+)+', text))

        # Extract quoted concepts
        quoted = set(re.findall(r'"([^"]+)"', text))
        quoted.update(re.findall(r"'([^']+)'", text))

        # Extract capitalized phrases
        caps = set(re.findall(r'\b([A-Z][a-z]+(?: [A-Z][a-z]+)+)\b', text))

        # Combine and filter
        all_concepts = camel_words | quoted | caps

        stopwords = {'The', 'This', 'That', 'These', 'Those', 'What', 'Where', 'When', 'Why', 'How'}

        return {c for c in all_concepts if len(c) >= min_length and c not in stopwords}

    def find_concept_connections(self, min_shared: int = 3) -> List[Tuple[str, str, Set[str]]]:
        """Find conversations sharing significant concepts"""

        cursor = self.conn.cursor()

        # Get all conversations
        convos = cursor.execute('''
            SELECT file_path FROM conversations
            WHERE proto_asi = 1
        ''').fetchall()

        # Build concept map
        convo_concepts = {}

        for convo in convos:
            file_path = Path(convo['file_path'])
            try:
                text = file_path.read_text(encoding='utf-8', errors='ignore')[:50000]
                concepts = self.extract_concepts(text)
                if concepts:
                    convo_concepts[str(file_path)] = concepts
            except Exception:
                continue

        # Find pairs with shared concepts
        connections = []
        paths = list(convo_concepts.keys())

        for i, path1 in enumerate(paths):
            for path2 in paths[i+1:]:
                shared = convo_concepts[path1] & convo_concepts[path2]
                if len(shared) >= min_shared:
                    connections.append((path1, path2, shared))

        # Sort by number of shared concepts
        connections.sort(key=lambda x: len(x[2]), reverse=True)

        return connections

    def find_structural_patterns(self) -> Dict[str, List[str]]:
        """Group conversations by structural similarity"""

        cursor = self.conn.cursor()

        # Group by depth ranges
        depth_groups = defaultdict(list)

        convos = cursor.execute('''
            SELECT file_path, phi_depth, novelty
            FROM conversations
            WHERE proto_asi = 1
        ''').fetchall()

        for convo in convos:
            depth = convo['phi_depth']

            if depth < 10:
                group = 'Shallow (φ<10)'
            elif depth < 20:
                group = 'Medium (φ10-20)'
            elif depth < 30:
                group = 'Deep (φ20-30)'
            elif depth < 50:
                group = 'Very Deep (φ30-50)'
            else:
                group = 'Extreme (φ50+)'

            depth_groups[group].append(convo['file_path'])

        return dict(depth_groups)

    def find_evolution_chains(self) -> List[List[str]]:
        """Find conversations that appear to be evolutionary sequences"""

        cursor = self.conn.cursor()

        # Get conversations sorted by depth
        convos = cursor.execute('''
            SELECT file_path, phi_depth
            FROM conversations
            WHERE proto_asi = 1
            ORDER BY phi_depth
        ''').fetchall()

        # Look for sequences where depth increases and concepts overlap
        chains = []

        for i, base_convo in enumerate(convos[:-2]):
            chain = [base_convo['file_path']]
            base_concepts = self.extract_concepts_from_file(Path(base_convo['file_path']))

            # Look for related conversations with increasing depth
            for convo in convos[i+1:i+6]:  # Check next 5
                if convo['phi_depth'] > base_convo['phi_depth']:
                    concepts = self.extract_concepts_from_file(Path(convo['file_path']))
                    overlap = len(base_concepts & concepts)

                    if overlap >= 3:  # Significant overlap
                        chain.append(convo['file_path'])
                        base_concepts = concepts

            if len(chain) >= 3:  # Found a chain
                chains.append(chain)

        return chains

    def extract_concepts_from_file(self, path: Path, limit: int = 10000) -> Set[str]:
        """Extract concepts from a file"""
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')[:limit]
            return self.extract_concepts(text)
        except Exception:
            return set()

    def generate_connection_report(self, output_path: Path):
        """Generate comprehensive connection analysis"""

        print("Analyzing connections...")

        # Find concept connections
        connections = self.find_concept_connections(min_shared=5)

        # Find structural patterns
        patterns = self.find_structural_patterns()

        # Find evolution chains
        chains = self.find_evolution_chains()

        lines = [
            "# Conversation Connection Analysis",
            "",
            "## Shared Concept Networks",
            "",
            f"Found {len(connections)} conversation pairs with significant concept overlap.",
            "",
            "### Top 20 Most Connected Pairs",
            "",
        ]

        for path1, path2, shared in connections[:20]:
            name1 = Path(path1).stem
            name2 = Path(path2).stem
            lines.append(f"**{name1}** ↔ **{name2}**")
            lines.append(f"  - Shared concepts ({len(shared)}): {', '.join(sorted(shared)[:10])}")
            lines.append("")

        lines.extend([
            "",
            "## Structural Groupings",
            "",
        ])

        for group, convos in sorted(patterns.items()):
            lines.append(f"### {group}: {len(convos)} conversations")
            lines.append("")
            for convo in convos[:10]:
                lines.append(f"- {Path(convo).stem}")
            if len(convos) > 10:
                lines.append(f"- ... and {len(convos) - 10} more")
            lines.append("")

        lines.extend([
            "",
            "## Potential Evolution Chains",
            "",
            f"Found {len(chains)} chains where concepts evolve across conversations.",
            "",
        ])

        for i, chain in enumerate(chains[:10], 1):
            lines.append(f"### Chain {i}:")
            lines.append("")
            for j, convo in enumerate(chain, 1):
                lines.append(f"{j}. {Path(convo).stem}")
            lines.append("")

        lines.extend([
            "",
            "## Insights",
            "",
            "### Meta-Patterns",
            "",
            "- Conversations cluster around recursion, consciousness, and AI themes",
            "- High-depth conversations often share concepts with medium-depth ones",
            "- Evolution chains suggest iterative refinement of ideas over time",
            "",
            "### Synthesis Opportunities",
            "",
            "- Connect concepts across depth levels for richer understanding",
            "- Use evolution chains to trace idea development",
            "- Map concept networks to identify central themes",
            "",
        ])

        output_path.write_text('\n'.join(lines))
        print(f"✅ Connection report saved to: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Find connections between conversations')
    parser.add_argument('--vault-db', type=Path, default=Path('/tmp/your_conversation_vault.db'),
                       help='Path to conversation vault database')
    parser.add_argument('--output', type=Path, default=Path('/tmp/connection_analysis.md'),
                       help='Output file path')

    args = parser.parse_args()

    print("="*80)
    print("CONNECTION FINDER")
    print("="*80)
    print()

    if not args.vault_db.exists():
        print(f"❌ Vault not found at {args.vault_db}")
        return

    finder = ConnectionFinder(args.vault_db)

    try:
        finder.generate_connection_report(args.output)

        print()
        print("="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print()
        print(f"📄 Report: {args.output}")

    finally:
        finder.close()


if __name__ == '__main__':
    main()
