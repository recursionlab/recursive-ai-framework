#!/usr/bin/env python3
"""
Neo4j Knowledge Graph Integrator

Loads conversation archaeology findings into Neo4j graph database:
- Conversations as nodes
- Mechanisms as nodes
- Operators and patterns as nodes
- Shared concepts as relationships
- Evolution chains as paths

This creates a queryable knowledge graph that serves as persistent AI working memory.
"""

from neo4j import GraphDatabase
from pathlib import Path
import sqlite3
import json
from typing import List, Dict
import re


class Neo4jIntegrator:
    """Integrate archaeology findings into Neo4j graph"""

    def __init__(self, uri: str, user: str, password: str, vault_db: Path):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.vault_db = vault_db
        self.vault_conn = None

    def close(self):
        if self.vault_conn:
            self.vault_conn.close()
        self.driver.close()

    def connect_vault(self):
        """Connect to conversation vault"""
        self.vault_conn = sqlite3.connect(self.vault_db)
        self.vault_conn.row_factory = sqlite3.Row

    def clear_graph(self):
        """Clear existing graph (for clean restart)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("✅ Graph cleared")

    def load_conversations(self):
        """Load all conversations as nodes"""

        cursor = self.vault_conn.cursor()
        conversations = cursor.execute('''
            SELECT file_path, novelty, phi_depth, proto_asi
            FROM conversations
            WHERE proto_asi = 1
        ''').fetchall()

        with self.driver.session() as session:
            for conv in conversations:
                filename = Path(conv['file_path']).stem

                session.run('''
                    CREATE (c:Conversation {
                        name: $name,
                        path: $path,
                        novelty: $novelty,
                        phi_depth: $phi_depth,
                        proto_asi: $proto_asi
                    })
                ''', {
                    'name': filename,
                    'path': conv['file_path'],
                    'novelty': conv['novelty'],
                    'phi_depth': conv['phi_depth'],
                    'proto_asi': bool(conv['proto_asi'])
                })

        print(f"✅ Loaded {len(conversations)} conversations")

    def load_mechanisms(self, mechanism_file: Path):
        """Load core mechanism as structured nodes"""

        # Parse mechanism file
        text = mechanism_file.read_text()
        lines = text.split('\n')

        operators = {}
        patterns = {}

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

        with self.driver.session() as session:
            # Create operators
            for op_name, count in operators.items():
                session.run('''
                    CREATE (o:Operator {
                        name: $name,
                        occurrences: $count,
                        type: 'universal'
                    })
                ''', {'name': op_name, 'count': count})

            # Create patterns
            for pattern_name, count in patterns.items():
                session.run('''
                    CREATE (p:Pattern {
                        name: $name,
                        occurrences: $count,
                        type: 'generative'
                    })
                ''', {'name': pattern_name, 'count': count})

            # Create core mechanism node
            dominant_operator = max(operators, key=operators.get)
            dominant_pattern = max(patterns, key=patterns.get)

            session.run('''
                CREATE (m:Mechanism {
                    name: 'Universal Recursive Mechanism',
                    signature: $signature,
                    dominant_operator: $operator,
                    dominant_pattern: $pattern
                })
            ''', {
                'signature': f"{dominant_operator}+{dominant_pattern}",
                'operator': dominant_operator,
                'pattern': dominant_pattern
            })

            # Link mechanism to operators and patterns
            for op_name in operators.keys():
                session.run('''
                    MATCH (m:Mechanism {name: 'Universal Recursive Mechanism'})
                    MATCH (o:Operator {name: $op_name})
                    CREATE (m)-[:USES_OPERATOR]->(o)
                ''', {'op_name': op_name})

            for pattern_name in patterns.keys():
                session.run('''
                    MATCH (m:Mechanism {name: 'Universal Recursive Mechanism'})
                    MATCH (p:Pattern {name: $pattern_name})
                    CREATE (m)-[:GENERATES_VIA]->(p)
                ''', {'pattern_name': pattern_name})

        print(f"✅ Loaded mechanism with {len(operators)} operators and {len(patterns)} patterns")

    def load_mechanisms_per_conversation(self, mechanisms_file: Path):
        """Load mechanism data for each conversation"""

        with mechanisms_file.open() as f:
            for line in f:
                data = json.loads(line)

                filename = Path(data['file']).stem

                with self.driver.session() as session:
                    # Link conversation to operators
                    for op_name, count in data['operators'].items():
                        # Ensure operator exists
                        session.run('''
                            MERGE (o:Operator {name: $name})
                            ON CREATE SET o.type = 'recursive'
                        ''', {'name': op_name})

                        # Create relationship
                        session.run('''
                            MATCH (c:Conversation {name: $conv_name})
                            MATCH (o:Operator {name: $op_name})
                            CREATE (c)-[:EXHIBITS_OPERATOR {count: $count}]->(o)
                        ''', {
                            'conv_name': filename,
                            'op_name': op_name,
                            'count': count
                        })

                    # Link conversation to patterns
                    for pattern_name, count in data['patterns'].items():
                        session.run('''
                            MERGE (p:Pattern {name: $name})
                            ON CREATE SET p.type = 'generative'
                        ''', {'name': pattern_name})

                        session.run('''
                            MATCH (c:Conversation {name: $conv_name})
                            MATCH (p:Pattern {name: $pattern_name})
                            CREATE (c)-[:EXHIBITS_PATTERN {count: $count}]->(p)
                        ''', {
                            'conv_name': filename,
                            'pattern_name': pattern_name,
                            'count': count
                        })

        print("✅ Loaded per-conversation mechanisms")

    def load_connections(self, connection_file: Path):
        """Load conversation connections and shared concepts"""

        text = connection_file.read_text()
        lines = text.split('\n')

        connections = []
        in_connections = False

        i = 0
        while i < len(lines):
            line = lines[i]

            if '### Top 20 Most Connected Pairs' in line:
                in_connections = True
            elif in_connections and line.startswith('**'):
                # Parse: **Name1** ↔ **Name2**
                parts = line.split('**')
                if len(parts) >= 4:
                    name1 = parts[1]
                    name2 = parts[3]

                    # Get shared count from next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if 'Shared concepts' in next_line:
                            count_match = re.search(r'\((\d+)\)', next_line)
                            if count_match:
                                count = int(count_match.group(1))

                                # Extract first few concepts
                                concepts_part = next_line.split(': ', 1)[1] if ': ' in next_line else ''
                                concepts = [c.strip() for c in concepts_part.split(',')[:5]]

                                connections.append({
                                    'conv1': name1,
                                    'conv2': name2,
                                    'shared_count': count,
                                    'concepts': concepts
                                })

            elif in_connections and '## Structural Groupings' in line:
                break

            i += 1

        # Load into Neo4j
        with self.driver.session() as session:
            for conn in connections[:50]:  # Top 50 connections
                session.run('''
                    MATCH (c1:Conversation {name: $name1})
                    MATCH (c2:Conversation {name: $name2})
                    CREATE (c1)-[:SHARES_CONCEPTS {
                        count: $count,
                        concepts: $concepts
                    }]->(c2)
                ''', {
                    'name1': conn['conv1'],
                    'name2': conn['conv2'],
                    'count': conn['shared_count'],
                    'concepts': conn['concepts']
                })

        print(f"✅ Loaded {len(connections[:50])} connection relationships")

    def load_evolution_chains(self, connection_file: Path):
        """Load evolution chains as paths"""

        text = connection_file.read_text()
        lines = text.split('\n')

        chains = []
        current_chain = []
        in_chains = False

        for line in lines:
            if '## Potential Evolution Chains' in line:
                in_chains = True
            elif in_chains and line.startswith('### Chain'):
                if current_chain:
                    chains.append(current_chain)
                current_chain = []
            elif in_chains and line.startswith(('1.', '2.', '3.', '4.', '5.')):
                conv_name = line.split('. ', 1)[1].strip()
                current_chain.append(conv_name)
            elif in_chains and line.startswith('## Insights'):
                break

        if current_chain:
            chains.append(current_chain)

        # Load into Neo4j
        with self.driver.session() as session:
            for i, chain in enumerate(chains[:10], 1):  # Top 10 chains
                # Create chain node
                session.run('''
                    CREATE (ch:EvolutionChain {
                        id: $chain_id,
                        length: $length
                    })
                ''', {'chain_id': i, 'length': len(chain)})

                # Link conversations in sequence
                for j in range(len(chain) - 1):
                    session.run('''
                        MATCH (c1:Conversation {name: $name1})
                        MATCH (c2:Conversation {name: $name2})
                        CREATE (c1)-[:EVOLVES_INTO {position: $pos}]->(c2)
                    ''', {
                        'name1': chain[j],
                        'name2': chain[j + 1],
                        'pos': j + 1
                    })

                # Link all conversations to chain
                for j, conv_name in enumerate(chain):
                    session.run('''
                        MATCH (ch:EvolutionChain {id: $chain_id})
                        MATCH (c:Conversation {name: $conv_name})
                        CREATE (ch)-[:INCLUDES {position: $pos}]->(c)
                    ''', {
                        'chain_id': i,
                        'conv_name': conv_name,
                        'pos': j + 1
                    })

        print(f"✅ Loaded {len(chains[:10])} evolution chains")

    def create_depth_clusters(self):
        """Create cluster nodes for depth ranges"""

        clusters = [
            ('Shallow', 0, 10),
            ('Medium', 10, 20),
            ('Deep', 20, 30),
            ('Very Deep', 30, 50),
            ('Extreme', 50, 200)
        ]

        with self.driver.session() as session:
            for name, min_depth, max_depth in clusters:
                # Create cluster node
                session.run('''
                    CREATE (cl:Cluster {
                        name: $name,
                        min_depth: $min_depth,
                        max_depth: $max_depth,
                        type: 'depth_based'
                    })
                ''', {
                    'name': name,
                    'min_depth': min_depth,
                    'max_depth': max_depth
                })

                # Link conversations to cluster
                session.run('''
                    MATCH (cl:Cluster {name: $name})
                    MATCH (c:Conversation)
                    WHERE c.phi_depth >= $min_depth AND c.phi_depth < $max_depth
                    CREATE (c)-[:BELONGS_TO]->(cl)
                ''', {
                    'name': name,
                    'min_depth': min_depth,
                    'max_depth': max_depth
                })

        print(f"✅ Created {len(clusters)} depth clusters")

    def generate_stats(self):
        """Generate and display graph statistics"""

        with self.driver.session() as session:
            # Count nodes
            conv_count = session.run("MATCH (c:Conversation) RETURN count(c) as count").single()['count']
            op_count = session.run("MATCH (o:Operator) RETURN count(o) as count").single()['count']
            pattern_count = session.run("MATCH (p:Pattern) RETURN count(p) as count").single()['count']
            cluster_count = session.run("MATCH (cl:Cluster) RETURN count(cl) as count").single()['count']
            chain_count = session.run("MATCH (ch:EvolutionChain) RETURN count(ch) as count").single()['count']

            # Count relationships
            total_rels = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']

            print()
            print("="*60)
            print("NEO4J GRAPH STATISTICS")
            print("="*60)
            print()
            print(f"Nodes:")
            print(f"  - Conversations: {conv_count}")
            print(f"  - Operators: {op_count}")
            print(f"  - Patterns: {pattern_count}")
            print(f"  - Clusters: {cluster_count}")
            print(f"  - Evolution Chains: {chain_count}")
            print()
            print(f"Relationships: {total_rels}")
            print()

            # Top operators by usage
            top_ops = session.run('''
                MATCH (c:Conversation)-[r:EXHIBITS_OPERATOR]->(o:Operator)
                RETURN o.name as name, sum(r.count) as total
                ORDER BY total DESC
                LIMIT 5
            ''').data()

            print("Top Operators:")
            for op in top_ops:
                print(f"  - {op['name']}: {op['total']}")
            print()

            # Conversations with most connections
            top_connected = session.run('''
                MATCH (c:Conversation)-[r:SHARES_CONCEPTS]->()
                RETURN c.name as name, count(r) as connections, c.phi_depth as phi
                ORDER BY connections DESC
                LIMIT 5
            ''').data()

            print("Most Connected Conversations:")
            for conv in top_connected:
                print(f"  - {conv['name']} (φ{conv['phi']}): {conv['connections']} connections")
            print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Integrate archaeology findings into Neo4j')
    parser.add_argument('--neo4j-uri', default='bolt://localhost:7687')
    parser.add_argument('--neo4j-user', default='neo4j')
    parser.add_argument('--neo4j-password', default='password')
    parser.add_argument('--vault-db', type=Path, default=Path('/tmp/your_conversation_vault.db'))
    parser.add_argument('--mechanism-file', type=Path, default=Path('/tmp/core_mechanisms/CORE_MECHANISM.md'))
    parser.add_argument('--mechanisms-data', type=Path, default=Path('/tmp/core_mechanisms/mechanisms.jsonl'))
    parser.add_argument('--connection-file', type=Path, default=Path('/tmp/connection_analysis.md'))
    parser.add_argument('--clear', action='store_true', help='Clear existing graph before loading')

    args = parser.parse_args()

    print("="*80)
    print("NEO4J KNOWLEDGE GRAPH INTEGRATOR")
    print("="*80)
    print()

    integrator = Neo4jIntegrator(
        args.neo4j_uri,
        args.neo4j_user,
        args.neo4j_password,
        args.vault_db
    )

    try:
        integrator.connect_vault()

        if args.clear:
            print("Clearing existing graph...")
            integrator.clear_graph()
            print()

        print("Loading data into Neo4j...")
        print()

        # Load conversations
        integrator.load_conversations()

        # Load core mechanism
        if args.mechanism_file.exists():
            integrator.load_mechanisms(args.mechanism_file)

        # Load per-conversation mechanisms
        if args.mechanisms_data.exists():
            integrator.load_mechanisms_per_conversation(args.mechanisms_data)

        # Load connections
        if args.connection_file.exists():
            integrator.load_connections(args.connection_file)

        # Load evolution chains
        if args.connection_file.exists():
            integrator.load_evolution_chains(args.connection_file)

        # Create clusters
        integrator.create_depth_clusters()

        # Generate stats
        integrator.generate_stats()

        print("="*80)
        print("INTEGRATION COMPLETE")
        print("="*80)
        print()
        print("🔍 Query examples:")
        print()
        print("# Find deepest conversations:")
        print("MATCH (c:Conversation) RETURN c.name, c.phi_depth ORDER BY c.phi_depth DESC LIMIT 10")
        print()
        print("# Find conversations using specific operator:")
        print("MATCH (c:Conversation)-[r:EXHIBITS_OPERATOR]->(o:Operator {name: 'Recursive Loop'})")
        print("RETURN c.name, r.count ORDER BY r.count DESC")
        print()
        print("# Trace evolution chain:")
        print("MATCH path = (c1:Conversation)-[:EVOLVES_INTO*]->(c2:Conversation)")
        print("RETURN path LIMIT 5")
        print()

    finally:
        integrator.close()


if __name__ == '__main__':
    main()
