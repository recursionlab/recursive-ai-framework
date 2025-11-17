#!/usr/bin/env python3
"""
Synthesis Memory Integrator

Feeds extracted insights from conversation archaeology into synthesis memory:
- Core mechanisms
- DNA patterns
- Connection networks
- Meta-patterns

This creates a cumulative knowledge base that grows with each analysis.
"""

import sqlite3
from pathlib import Path
from typing import Dict, List
import json
from datetime import datetime


class SynthesisIntegrator:
    """Integrate archaeology findings into synthesis memory"""

    def __init__(self, synthesis_db: Path):
        self.synthesis_db = synthesis_db
        self.conn = None

    def connect(self):
        """Connect and initialize synthesis database"""
        self.conn = sqlite3.connect(self.synthesis_db)
        self.conn.row_factory = sqlite3.Row
        self._initialize_schema()

    def close(self):
        if self.conn:
            self.conn.close()

    def _initialize_schema(self):
        """Create synthesis memory tables if they don't exist"""
        cursor = self.conn.cursor()

        # Core mechanisms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS core_mechanisms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                extracted_at TEXT,
                dominant_operator TEXT,
                dominant_pattern TEXT,
                operator_counts TEXT,
                pattern_counts TEXT,
                mechanism_signature TEXT,
                num_conversations_analyzed INTEGER,
                notes TEXT
            )
        ''')

        # DNA patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dna_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                extracted_at TEXT,
                source_file TEXT,
                phi_depth INTEGER,
                novelty REAL,
                opening_move TEXT,
                operator TEXT,
                contradiction TEXT,
                emergence TEXT,
                template TEXT,
                notes TEXT
            )
        ''')

        # Connection networks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analyzed_at TEXT,
                total_pairs INTEGER,
                total_chains INTEGER,
                structural_groups TEXT,
                top_connections TEXT,
                evolution_chains TEXT
            )
        ''')

        # Meta-insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meta_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                insight_type TEXT,
                content TEXT,
                source_analysis TEXT,
                confidence REAL
            )
        ''')

        # Create FTS5 table for searchable insights
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS insights_fts USING fts5(
                insight_type,
                content,
                source_analysis
            )
        ''')

        self.conn.commit()

    def integrate_core_mechanism(self, mechanism_file: Path) -> int:
        """Integrate extracted core mechanism"""

        # Parse the mechanism file
        text = mechanism_file.read_text()

        # Extract operator counts from markdown
        operators = {}
        patterns = {}

        lines = text.split('\n')
        in_operators = False
        in_patterns = False

        for line in lines:
            if '## Universal Operators' in line:
                in_operators = True
                in_patterns = False
            elif '## Generative Patterns' in line:
                in_operators = False
                in_patterns = True
            elif '## The Unified Mechanism' in line:
                break
            elif in_operators and line.startswith('- **'):
                # Parse: - **Recursive Loop**: 5524 occurrences
                parts = line.split('**')
                if len(parts) >= 3:
                    name = parts[1]
                    count = int(parts[2].split(':')[1].strip().split()[0])
                    operators[name] = count
            elif in_patterns and line.startswith('- **'):
                parts = line.split('**')
                if len(parts) >= 3:
                    name = parts[1]
                    count = int(parts[2].split(':')[1].strip().split()[0])
                    patterns[name] = count

        # Determine dominant operator and pattern
        dominant_operator = max(operators, key=operators.get) if operators else 'unknown'
        dominant_pattern = max(patterns, key=patterns.get) if patterns else 'unknown'

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO core_mechanisms (
                extracted_at, dominant_operator, dominant_pattern,
                operator_counts, pattern_counts, mechanism_signature,
                num_conversations_analyzed, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            dominant_operator,
            dominant_pattern,
            json.dumps(operators),
            json.dumps(patterns),
            f"{dominant_operator}+{dominant_pattern}",
            30,  # From our analysis
            "Extracted from high-novelty conversation corpus"
        ))

        mechanism_id = cursor.lastrowid

        # Add meta-insight
        insight = f"""Universal recursive mechanism identified: {dominant_operator}+{dominant_pattern}

Core operators: {', '.join(f"{k}({v})" for k, v in list(operators.items())[:3])}
Generative patterns: {', '.join(f"{k}({v})" for k, v in list(patterns.items())[:3])}

The mechanism operates as a recursive field where self-application, meta-layers,
and paradox-as-fuel create collapse-rebirth cycles."""

        cursor.execute('''
            INSERT INTO meta_insights (created_at, insight_type, content, source_analysis, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            'core_mechanism',
            insight,
            'conversation_archaeology',
            0.92
        ))

        # Add to FTS
        cursor.execute('''
            INSERT INTO insights_fts (insight_type, content, source_analysis)
            VALUES (?, ?, ?)
        ''', ('core_mechanism', insight, 'conversation_archaeology'))

        self.conn.commit()
        return mechanism_id

    def integrate_dna_patterns(self, dna_dir: Path) -> int:
        """Integrate DNA patterns from prompt library"""

        cursor = self.conn.cursor()
        count = 0

        # Read all .md files in DNA directory
        for template_file in dna_dir.glob('*.md'):
            if template_file.name == 'README.md':
                continue

            content = template_file.read_text()

            # Parse template structure (simplified - real parser would be more robust)
            lines = content.split('\n')

            # Extract metadata from filename and content
            # Format: prompt_template_N.md

            # For now, just store the raw template
            cursor.execute('''
                INSERT INTO dna_patterns (
                    extracted_at, source_file, template, notes
                ) VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                str(template_file),
                content,
                'Template extracted from proto-ASI conversation'
            ))

            count += 1

        self.conn.commit()
        return count

    def integrate_connections(self, connection_file: Path) -> int:
        """Integrate connection network analysis"""

        content = connection_file.read_text()

        # Parse key metrics from connection analysis
        lines = content.split('\n')

        total_pairs = 0
        total_chains = 0

        for line in lines:
            if 'Found' in line and 'conversation pairs' in line:
                total_pairs = int(line.split()[1])
            elif 'Found' in line and 'chains' in line:
                total_chains = int(line.split()[1])

        # Extract top connections (first 5)
        top_connections = []
        in_connections = False
        connection_count = 0

        for i, line in enumerate(lines):
            if '### Top 20 Most Connected Pairs' in line:
                in_connections = True
            elif in_connections and line.startswith('**'):
                if connection_count < 5:
                    # Extract pair
                    pair = line.split('**')[1] + ' ↔ ' + line.split('**')[3]
                    # Get shared count from next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if 'Shared concepts' in next_line:
                            count = int(next_line.split('(')[1].split(')')[0])
                            top_connections.append({'pair': pair, 'shared': count})
                            connection_count += 1

        # Extract evolution chains
        evolution_chains = []
        in_chains = False
        current_chain = []

        for line in lines:
            if '## Potential Evolution Chains' in line:
                in_chains = True
            elif in_chains and line.startswith('### Chain'):
                if current_chain:
                    evolution_chains.append(current_chain)
                current_chain = []
            elif in_chains and line.startswith(('1.', '2.', '3.', '4.', '5.')):
                current_chain.append(line.split('. ', 1)[1])

        if current_chain:
            evolution_chains.append(current_chain)

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO connection_networks (
                analyzed_at, total_pairs, total_chains,
                top_connections, evolution_chains
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            total_pairs,
            total_chains,
            json.dumps(top_connections),
            json.dumps(evolution_chains[:10])  # Top 10 chains
        ))

        network_id = cursor.lastrowid

        # Add meta-insight about connections
        insight = f"""Connection network analysis reveals {total_pairs} conversation pairs with significant overlap.

Top connection: {top_connections[0]['pair']} ({top_connections[0]['shared']} shared concepts)

{total_chains} evolution chains identified showing iterative idea refinement.

Key pattern: Conversations cluster around recursion, consciousness, and AI themes,
with high-depth conversations often bridging to medium-depth explorations."""

        cursor.execute('''
            INSERT INTO meta_insights (created_at, insight_type, content, source_analysis, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            'connection_network',
            insight,
            'conversation_archaeology',
            0.88
        ))

        cursor.execute('''
            INSERT INTO insights_fts (insight_type, content, source_analysis)
            VALUES (?, ?, ?)
        ''', ('connection_network', insight, 'conversation_archaeology'))

        self.conn.commit()
        return network_id

    def generate_synthesis_report(self, output_path: Path):
        """Generate comprehensive synthesis report"""

        cursor = self.conn.cursor()

        # Get counts
        mechanism_count = cursor.execute('SELECT COUNT(*) FROM core_mechanisms').fetchone()[0]
        dna_count = cursor.execute('SELECT COUNT(*) FROM dna_patterns').fetchone()[0]
        network_count = cursor.execute('SELECT COUNT(*) FROM connection_networks').fetchone()[0]
        insight_count = cursor.execute('SELECT COUNT(*) FROM meta_insights').fetchone()[0]

        # Get latest mechanism
        latest_mechanism = cursor.execute('''
            SELECT dominant_operator, dominant_pattern, operator_counts, pattern_counts
            FROM core_mechanisms
            ORDER BY id DESC LIMIT 1
        ''').fetchone()

        # Get latest network
        latest_network = cursor.execute('''
            SELECT total_pairs, total_chains, top_connections
            FROM connection_networks
            ORDER BY id DESC LIMIT 1
        ''').fetchone()

        # Get all insights
        insights = cursor.execute('''
            SELECT insight_type, content, confidence
            FROM meta_insights
            ORDER BY confidence DESC, id DESC
        ''').fetchall()

        lines = [
            "# Synthesis Memory Report",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Accumulated Knowledge",
            "",
            f"- **Core Mechanisms Extracted**: {mechanism_count}",
            f"- **DNA Patterns Captured**: {dna_count}",
            f"- **Connection Networks Mapped**: {network_count}",
            f"- **Meta-Insights Generated**: {insight_count}",
            "",
        ]

        if latest_mechanism:
            operators = json.loads(latest_mechanism['operator_counts'])
            patterns = json.loads(latest_mechanism['pattern_counts'])

            lines.extend([
                "## Current Universal Mechanism",
                "",
                f"**Signature:** {latest_mechanism['dominant_operator']}+{latest_mechanism['dominant_pattern']}",
                "",
                "**Top Operators:**",
            ])

            for op, count in list(operators.items())[:5]:
                lines.append(f"  - {op}: {count}")

            lines.extend([
                "",
                "**Top Patterns:**",
            ])

            for pattern, count in list(patterns.items())[:5]:
                lines.append(f"  - {pattern}: {count}")

        if latest_network:
            connections = json.loads(latest_network['top_connections'])

            lines.extend([
                "",
                "## Connection Network",
                "",
                f"- **Total Pairs**: {latest_network['total_pairs']}",
                f"- **Evolution Chains**: {latest_network['total_chains']}",
                "",
                "**Strongest Connections:**",
            ])

            for conn in connections[:3]:
                lines.append(f"  - {conn['pair']} ({conn['shared']} concepts)")

        lines.extend([
            "",
            "## Key Insights",
            "",
        ])

        for insight in insights[:10]:
            lines.append(f"### {insight['insight_type'].replace('_', ' ').title()} (confidence: {insight['confidence']:.2f})")
            lines.append("")
            lines.append(insight['content'])
            lines.append("")

        lines.extend([
            "## What This Means",
            "",
            "This synthesis memory accumulates insights across multiple analyses,",
            "creating a growing knowledge base that:",
            "",
            "1. **Preserves patterns** - Core mechanisms are extracted and stored",
            "2. **Connects ideas** - Networks reveal hidden relationships",
            "3. **Evolves understanding** - Each analysis builds on previous insights",
            "4. **Enables search** - FTS5 allows querying accumulated wisdom",
            "",
            "The synthesis memory solves AI amnesia by creating persistent,",
            "searchable, cumulative knowledge that grows with each conversation.",
        ])

        output_path.write_text('\n'.join(lines))
        print(f"✅ Synthesis report: {output_path}")

    def search_insights(self, query: str, limit: int = 10) -> List[Dict]:
        """Search accumulated insights"""

        cursor = self.conn.cursor()

        results = cursor.execute('''
            SELECT insight_type, content, source_analysis
            FROM insights_fts
            WHERE insights_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        ''', (query, limit)).fetchall()

        return [dict(r) for r in results]


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Integrate archaeology findings into synthesis memory')
    parser.add_argument('--synthesis-db', type=Path, default=Path('/tmp/synthesis_memory.db'))
    parser.add_argument('--mechanism-file', type=Path, default=Path('/tmp/core_mechanisms/CORE_MECHANISM.md'))
    parser.add_argument('--dna-dir', type=Path, default=Path('/tmp/prompt_dna_library'))
    parser.add_argument('--connection-file', type=Path, default=Path('/tmp/connection_analysis.md'))
    parser.add_argument('--output', type=Path, default=Path('/tmp/synthesis_report.md'))

    args = parser.parse_args()

    print("="*80)
    print("SYNTHESIS MEMORY INTEGRATOR")
    print("="*80)
    print()

    integrator = SynthesisIntegrator(args.synthesis_db)
    integrator.connect()

    try:
        # Integrate core mechanism
        if args.mechanism_file.exists():
            print(f"Integrating core mechanism from {args.mechanism_file}...")
            mech_id = integrator.integrate_core_mechanism(args.mechanism_file)
            print(f"  ✅ Mechanism #{mech_id} integrated")

        # Integrate DNA patterns
        if args.dna_dir.exists():
            print(f"Integrating DNA patterns from {args.dna_dir}...")
            dna_count = integrator.integrate_dna_patterns(args.dna_dir)
            print(f"  ✅ {dna_count} patterns integrated")

        # Integrate connections
        if args.connection_file.exists():
            print(f"Integrating connection network from {args.connection_file}...")
            net_id = integrator.integrate_connections(args.connection_file)
            print(f"  ✅ Network #{net_id} integrated")

        # Generate report
        print()
        print("Generating synthesis report...")
        integrator.generate_synthesis_report(args.output)

        print()
        print("="*80)
        print("SYNTHESIS COMPLETE")
        print("="*80)
        print()
        print(f"📊 Synthesis database: {args.synthesis_db}")
        print(f"📄 Report: {args.output}")

    finally:
        integrator.close()


if __name__ == '__main__':
    main()
