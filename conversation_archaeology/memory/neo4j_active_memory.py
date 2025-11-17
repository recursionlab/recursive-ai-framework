"""
Active Neo4j Memory Layer - Make AI ACTUALLY USE your knowledge graph

Problem:
- You have Neo4j with your knowledge loaded
- AI only queries when explicitly told "check the database"
- AI doesn't proactively use it to understand you
- Every session starts from zero

Solution:
- AI automatically queries Neo4j for relevant context
- Builds synthesis from graph data
- Stores synthesis in persistent memory (synthesis_memory.py)
- Loads synthesis at session start
- Updates understanding as new queries reveal patterns

This turns Neo4j from passive storage into active memory.
"""

from neo4j import GraphDatabase
from pathlib import Path
from typing import List, Dict, Optional, Any
import sys

sys.path.append(str(Path(__file__).parent))
from synthesis_memory import SynthesisMemory


class Neo4jActiveMemory:
    """
    Wrapper around Neo4j that actively uses the graph to build understanding

    Instead of:
        User: "Query the database about X"
        AI: [queries] "Here's what I found"

    This enables:
        AI: [automatically queries Neo4j about current topic]
        AI: [synthesizes with existing knowledge]
        AI: [stores synthesis in persistent memory]
        AI: "Based on your knowledge graph and previous insights..."
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 synthesis_db_path: Path):
        """
        Initialize active memory layer

        Args:
            neo4j_uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            synthesis_db_path: Path to synthesis memory database
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.synthesis = SynthesisMemory(synthesis_db_path)

        # Cache of recent queries to avoid redundant lookups
        self.query_cache = {}

    def close(self):
        self.driver.close()
        self.synthesis.close()

    def auto_contextualize(self, user_message: str) -> Dict[str, Any]:
        """
        Automatically query Neo4j for relevant context based on user message

        This is the key difference - AI calls this AUTOMATICALLY, not waiting
        for explicit "query database" command

        Returns context that AI should consider when responding
        """
        # Extract key terms from user message
        keywords = self._extract_keywords(user_message)

        # Query Neo4j for nodes/relationships matching keywords
        context = {
            'nodes': [],
            'relationships': [],
            'insights': [],
            'synthesis': None
        }

        with self.driver.session() as session:
            for keyword in keywords:
                # Find relevant nodes
                result = session.run("""
                    MATCH (n)
                    WHERE toLower(n.name) CONTAINS toLower($keyword)
                       OR toLower(n.description) CONTAINS toLower($keyword)
                       OR ANY(label IN labels(n) WHERE toLower(label) CONTAINS toLower($keyword))
                    RETURN n, labels(n) as labels
                    LIMIT 10
                """, keyword=keyword)

                for record in result:
                    node = dict(record['n'])
                    node['labels'] = record['labels']
                    context['nodes'].append(node)

                # Find relevant relationships
                result = session.run("""
                    MATCH (a)-[r]->(b)
                    WHERE toLower(type(r)) CONTAINS toLower($keyword)
                       OR toLower(a.name) CONTAINS toLower($keyword)
                       OR toLower(b.name) CONTAINS toLower($keyword)
                    RETURN a, r, b, type(r) as rel_type
                    LIMIT 10
                """, keyword=keyword)

                for record in result:
                    context['relationships'].append({
                        'source': dict(record['a']),
                        'relationship': record['rel_type'],
                        'target': dict(record['b']),
                        'properties': dict(record['r'])
                    })

        # Check synthesis memory for existing insights on these topics
        for keyword in keywords:
            existing_insights = self.synthesis.search_insights(keyword)
            context['insights'].extend([i.to_dict() for i in existing_insights])

        # Generate synthesis from graph patterns
        context['synthesis'] = self._synthesize_from_context(context, user_message)

        return context

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from user message"""
        # Simple implementation - in production, use NLP
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
                    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'how', 'why'}

        words = text.lower().split()
        keywords = [w.strip('.,!?;:') for w in words if w not in stopwords and len(w) > 3]
        return keywords[:5]  # Top 5 keywords

    def _synthesize_from_context(self, context: Dict, user_message: str) -> str:
        """
        Generate synthesis from Neo4j context

        This is what makes it "active" - AI doesn't just return raw data,
        it creates understanding
        """
        nodes_count = len(context['nodes'])
        rels_count = len(context['relationships'])
        insights_count = len(context['insights'])

        if nodes_count == 0 and rels_count == 0:
            return "No relevant context found in knowledge graph"

        synthesis_parts = []

        if nodes_count > 0:
            node_labels = set()
            for node in context['nodes']:
                node_labels.update(node.get('labels', []))
            synthesis_parts.append(
                f"Found {nodes_count} relevant concepts across domains: {', '.join(node_labels)}"
            )

        if rels_count > 0:
            rel_types = set(r['relationship'] for r in context['relationships'])
            synthesis_parts.append(
                f"Identified {rels_count} connections of types: {', '.join(rel_types)}"
            )

        if insights_count > 0:
            synthesis_parts.append(
                f"Retrieved {insights_count} previous insights on related topics"
            )

        return ". ".join(synthesis_parts)

    def learn_from_graph_pattern(self, pattern_query: str, topic: str,
                                 insight_statement: str, confidence: float = 0.7):
        """
        Extract a pattern from Neo4j and store as persistent insight

        This is how AI LEARNS from the graph over time
        """
        with self.driver.session() as session:
            result = session.run(pattern_query)
            evidence_count = sum(1 for _ in result)

        if evidence_count > 0:
            insight_id = self.synthesis.add_insight(topic, insight_statement, confidence)
            self.synthesis.add_evidence(
                insight_id,
                "neo4j_pattern",
                f"Pattern query: {pattern_query}\nMatches: {evidence_count}"
            )
            return insight_id
        return None

    def explore_neighborhood(self, node_name: str, depth: int = 2) -> Dict:
        """
        Explore graph neighborhood around a concept

        Useful for "what else is related to X?" queries
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (start)-[*1..{depth}]-(connected)
                WHERE toLower(start.name) = toLower($node_name)
                RETURN path
                LIMIT 50
            """.format(depth=depth), node_name=node_name)

            paths = []
            for record in result:
                path = record['path']
                paths.append({
                    'nodes': [dict(node) for node in path.nodes],
                    'relationships': [dict(rel) for rel in path.relationships]
                })

            return {'paths': paths, 'count': len(paths)}

    def get_schema_overview(self) -> Dict:
        """Get overview of what's in the Neo4j database"""
        with self.driver.session() as session:
            # Get node labels
            labels_result = session.run("CALL db.labels()")
            labels = [record[0] for record in labels_result]

            # Get relationship types
            rels_result = session.run("CALL db.relationshipTypes()")
            rel_types = [record[0] for record in rels_result]

            # Get counts
            node_count_result = session.run("MATCH (n) RETURN count(n) as count")
            node_count = node_count_result.single()['count']

            rel_count_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            rel_count = rel_count_result.single()['count']

            return {
                'node_labels': labels,
                'relationship_types': rel_types,
                'node_count': node_count,
                'relationship_count': rel_count
            }

    def auto_discover_patterns(self) -> List[Dict]:
        """
        Automatically discover interesting patterns in the graph

        This is what AI should run periodically to learn about your knowledge
        """
        patterns = []

        with self.driver.session() as session:
            # Pattern 1: Highly connected nodes (hubs)
            result = session.run("""
                MATCH (n)-[r]-()
                WITH n, count(r) as connections
                WHERE connections > 5
                RETURN n, connections
                ORDER BY connections DESC
                LIMIT 10
            """)

            hubs = []
            for record in result:
                node = dict(record['n'])
                node['connection_count'] = record['connections']
                hubs.append(node)

            if hubs:
                patterns.append({
                    'type': 'hubs',
                    'description': 'Highly connected concepts',
                    'data': hubs
                })

            # Pattern 2: Common relationship types
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
                LIMIT 10
            """)

            common_rels = [dict(record) for record in result]
            if common_rels:
                patterns.append({
                    'type': 'common_relationships',
                    'description': 'Most frequently used relationship types',
                    'data': common_rels
                })

            # Pattern 3: Isolated clusters
            result = session.run("""
                MATCH (n)
                WHERE NOT EXISTS((n)--())
                RETURN n
                LIMIT 10
            """)

            isolated = [dict(record['n']) for record in result]
            if isolated:
                patterns.append({
                    'type': 'isolated_nodes',
                    'description': 'Concepts not connected to anything',
                    'data': isolated
                })

        return patterns


class SessionStartup:
    """
    Run this at the START of every AI session

    This loads context from Neo4j + synthesis memory so AI starts with
    accumulated knowledge instead of amnesia
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 synthesis_db_path: Path):
        self.active_memory = Neo4jActiveMemory(
            neo4j_uri, neo4j_user, neo4j_password, synthesis_db_path
        )

    def load_session_context(self) -> str:
        """
        Load all relevant context for AI to start with

        Returns formatted string to inject into AI's initial context
        """
        # Get graph overview
        schema = self.active_memory.get_schema_overview()

        # Get existing insights
        insights = self.active_memory.synthesis.get_all_insights(min_confidence=0.6)

        # Auto-discover patterns
        patterns = self.active_memory.auto_discover_patterns()

        # Format as context string
        context = [
            "=== ACTIVE MEMORY CONTEXT (Loaded from Neo4j + Synthesis) ===\n",
            f"Knowledge Graph: {schema['node_count']} nodes, {schema['relationship_count']} relationships",
            f"Node Types: {', '.join(schema['node_labels'][:10])}",
            f"Relationship Types: {', '.join(schema['relationship_types'][:10])}\n",
            f"Accumulated Insights: {len(insights)}\n"
        ]

        if insights:
            context.append("Recent High-Confidence Insights:")
            for insight in insights[:5]:
                context.append(f"  - [{insight.confidence:.2f}] {insight.statement}")

        if patterns:
            context.append("\nGraph Patterns:")
            for pattern in patterns:
                context.append(f"  - {pattern['description']}: {len(pattern['data'])} items")

        context.append("\n=== Use auto_contextualize() automatically when relevant ===")

        return "\n".join(context)

    def close(self):
        self.active_memory.close()


if __name__ == '__main__':
    # Example: Load session context at startup
    # In production, this runs automatically when AI session starts

    print("Testing Neo4j Active Memory Layer")
    print("=" * 80)

    # These would come from environment variables
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "your_password"  # User should set this
    SYNTHESIS_DB = Path("/tmp/neo4j_synthesis_memory.db")

    try:
        startup = SessionStartup(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, SYNTHESIS_DB)
        context = startup.load_session_context()
        print(context)
        startup.close()
    except Exception as e:
        print(f"Error: {e}")
        print("\nTo use this, configure your Neo4j connection details:")
        print("  NEO4J_URI = bolt://localhost:7687")
        print("  NEO4J_USER = neo4j")
        print("  NEO4J_PASSWORD = your_password")
