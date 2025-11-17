"""
Neo4j as WORKING MEMORY - AI reads AND writes to build understanding over time

The missing piece: AI must WRITE to Neo4j, not just read from it

Flow:
1. Session starts → AI reads current graph state
2. User says something → AI automatically queries relevant context
3. AI learns something new → WRITES new node/relationship to graph
4. AI realizes connection → CREATES relationship between existing nodes
5. AI's understanding deepens → UPDATES node properties
6. Next session → Graph contains ALL accumulated knowledge

The graph itself IS the persistent memory. No separate database needed.
"""

from neo4j import GraphDatabase
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib


class Neo4jWorkingMemory:
    """
    Neo4j as active working memory that AI reads from AND writes to

    Key methods:
    - remember(): Store new knowledge in graph
    - connect(): Link concepts together
    - deepen(): Update understanding of existing concept
    - recall(): Retrieve relevant context
    - reflect(): Discover patterns in accumulated knowledge
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._ensure_constraints()

    def _ensure_constraints(self):
        """Create constraints/indexes for efficient querying"""
        with self.driver.session() as session:
            # Unique constraint on concept IDs
            try:
                session.run("""
                    CREATE CONSTRAINT concept_id IF NOT EXISTS
                    FOR (c:Concept) REQUIRE c.id IS UNIQUE
                """)
            except:
                pass  # Constraint might already exist

            # Index on names for fast lookup
            try:
                session.run("""
                    CREATE INDEX concept_name IF NOT EXISTS
                    FOR (c:Concept) ON (c.name)
                """)
            except:
                pass

    def remember(self, concept: str, properties: Dict[str, Any] = None,
                 labels: List[str] = None, source: str = "conversation") -> str:
        """
        Store new knowledge in graph

        Args:
            concept: Name of the concept
            properties: Additional properties (description, confidence, etc.)
            labels: Additional labels beyond 'Concept'
            source: Where this knowledge came from

        Returns:
            concept_id: Unique ID of created/updated node
        """
        # Generate stable ID from concept name
        concept_id = hashlib.sha256(concept.lower().encode()).hexdigest()[:16]

        props = properties or {}
        props.update({
            'name': concept,
            'id': concept_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'source': source,
            'access_count': 0
        })

        # Build label string
        label_str = ':Concept'
        if labels:
            label_str += ':' + ':'.join(labels)

        with self.driver.session() as session:
            # Merge (create if not exists, update if exists)
            result = session.run(f"""
                MERGE (c{label_str} {{id: $id}})
                ON CREATE SET c = $props
                ON MATCH SET c.updated_at = $updated_at, c.access_count = c.access_count + 1
                RETURN c.id as id
            """, id=concept_id, props=props, updated_at=datetime.now().isoformat())

            return result.single()['id']

    def connect(self, from_concept: str, to_concept: str, relationship: str,
                properties: Dict[str, Any] = None) -> bool:
        """
        Create relationship between concepts

        This is how AI builds the knowledge graph as it learns connections

        Args:
            from_concept: Source concept name
            to_concept: Target concept name
            relationship: Type of relationship (e.g., "RELATES_TO", "IMPLEMENTS", "CONTRADICTS")
            properties: Relationship properties (strength, confidence, etc.)

        Returns:
            success: Whether relationship was created
        """
        from_id = hashlib.sha256(from_concept.lower().encode()).hexdigest()[:16]
        to_id = hashlib.sha256(to_concept.lower().encode()).hexdigest()[:16]

        props = properties or {}
        props.update({
            'created_at': datetime.now().isoformat(),
            'strength': props.get('strength', 1.0),
            'confidence': props.get('confidence', 0.7)
        })

        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (a:Concept {{id: $from_id}})
                MATCH (b:Concept {{id: $to_id}})
                MERGE (a)-[r:{relationship}]->(b)
                ON CREATE SET r = $props
                ON MATCH SET r.strength = r.strength + $increment
                RETURN r
            """, from_id=from_id, to_id=to_id, props=props, increment=0.1)

            return result.single() is not None

    def deepen(self, concept: str, new_understanding: Dict[str, Any]):
        """
        Update/deepen understanding of existing concept

        AI calls this when it learns more about something it already knows

        Args:
            concept: Concept name
            new_understanding: Properties to update/add
        """
        concept_id = hashlib.sha256(concept.lower().encode()).hexdigest()[:16]

        # Add timestamp
        new_understanding['updated_at'] = datetime.now().isoformat()

        with self.driver.session() as session:
            # Build SET clause dynamically
            set_clauses = [f"c.{key} = ${key}" for key in new_understanding.keys()]
            set_str = ", ".join(set_clauses)

            session.run(f"""
                MATCH (c:Concept {{id: $id}})
                SET {set_str}
            """, id=concept_id, **new_understanding)

    def recall(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Retrieve relevant concepts from working memory

        AI calls this automatically when processing user messages

        Args:
            query: Search query (concept name, keywords, etc.)
            max_results: Maximum number of results to return

        Returns:
            List of relevant concepts with their properties and connections
        """
        with self.driver.session() as session:
            # Search by name or description
            result = session.run("""
                MATCH (c:Concept)
                WHERE toLower(c.name) CONTAINS toLower($query)
                   OR toLower(c.description) CONTAINS toLower($query)

                // Get connected concepts
                OPTIONAL MATCH (c)-[r]-(connected:Concept)

                // Update access count
                SET c.access_count = c.access_count + 1

                WITH c, collect({
                    concept: connected.name,
                    relationship: type(r),
                    direction: CASE WHEN startNode(r) = c THEN 'outgoing' ELSE 'incoming' END
                }) as connections

                RETURN c as concept, connections
                ORDER BY c.access_count DESC
                LIMIT $limit
            """, query=query, limit=max_results)

            concepts = []
            for record in result:
                concept_dict = dict(record['concept'])
                concept_dict['connections'] = record['connections']
                concepts.append(concept_dict)

            return concepts

    def reflect(self) -> Dict[str, Any]:
        """
        Discover patterns in accumulated knowledge

        AI should run this periodically to learn about its own memory

        Returns:
            Insights about the knowledge graph structure
        """
        with self.driver.session() as session:
            # Most central concepts (PageRank-like)
            central = session.run("""
                MATCH (c:Concept)-[r]-()
                WITH c, count(r) as connections
                RETURN c.name as concept, connections
                ORDER BY connections DESC
                LIMIT 5
            """)

            # Most frequently accessed
            frequent = session.run("""
                MATCH (c:Concept)
                WHERE c.access_count > 0
                RETURN c.name as concept, c.access_count as accesses
                ORDER BY accesses DESC
                LIMIT 5
            """)

            # Recent learnings
            recent = session.run("""
                MATCH (c:Concept)
                RETURN c.name as concept, c.created_at as created
                ORDER BY created DESC
                LIMIT 5
            """)

            # Relationship patterns
            rel_patterns = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as relationship, count(r) as count
                ORDER BY count DESC
                LIMIT 5
            """)

            return {
                'most_central': [dict(r) for r in central],
                'most_accessed': [dict(r) for r in frequent],
                'recently_learned': [dict(r) for r in recent],
                'relationship_patterns': [dict(r) for r in rel_patterns]
            }

    def auto_process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Automatically process user message using working memory

        This is what AI calls for EVERY message:
        1. Recall relevant context
        2. Detect new concepts
        3. Remember new things
        4. Connect related concepts

        Returns:
            context: What AI should know for this message
            actions_taken: What was added/updated in graph
        """
        # Extract keywords
        keywords = self._extract_keywords(user_message)

        # Recall relevant concepts
        context = []
        for keyword in keywords:
            recalled = self.recall(keyword, max_results=3)
            context.extend(recalled)

        # Detect if user is introducing new concept
        # (Simple heuristic - in production, use NLP)
        new_concepts = []
        if any(indicator in user_message.lower() for indicator in
               ['is when', 'means', 'refers to', 'is a', 'defined as']):
            # User is defining something new
            # Extract concept (would use NLP in production)
            for keyword in keywords:
                if len(keyword) > 4:  # Reasonable concept name
                    concept_id = self.remember(
                        concept=keyword,
                        properties={
                            'description': user_message[:200],
                            'confidence': 0.6
                        },
                        labels=['UserDefined']
                    )
                    new_concepts.append(keyword)

        # Detect connections between concepts
        # If message mentions multiple known concepts, link them
        connections_made = []
        if len(context) >= 2:
            # Link concepts that appear in same message
            for i, concept1 in enumerate(context[:3]):
                for concept2 in context[i+1:4]:
                    if concept1['name'] != concept2['name']:
                        self.connect(
                            concept1['name'],
                            concept2['name'],
                            'DISCUSSED_WITH',
                            properties={'context': user_message[:100]}
                        )
                        connections_made.append(f"{concept1['name']} <-> {concept2['name']}")

        return {
            'context': context,
            'new_concepts_learned': new_concepts,
            'connections_made': connections_made,
            'action': 'INJECT_CONTEXT_AND_CONTINUE_LEARNING'
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords"""
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
                    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'how', 'why', 'when'}

        words = text.lower().split()
        keywords = [w.strip('.,!?;:()[]{}') for w in words if w not in stopwords and len(w) > 3]
        return keywords[:10]

    def export_for_ai_context(self, limit: int = 50) -> str:
        """
        Export current graph state as text for AI to understand

        This runs at session startup to load accumulated knowledge
        """
        with self.driver.session() as session:
            # Get overview
            stats = session.run("""
                MATCH (c:Concept)
                OPTIONAL MATCH ()-[r]->()
                RETURN count(DISTINCT c) as concepts, count(r) as relationships
            """).single()

            # Get reflection
            reflection = self.reflect()

            # Format as readable text
            lines = [
                "=== WORKING MEMORY STATE ===",
                f"Knowledge Graph: {stats['concepts']} concepts, {stats['relationships']} connections\n",
                "Most Central Concepts:"
            ]

            for item in reflection['most_central']:
                lines.append(f"  - {item['concept']} ({item['connections']} connections)")

            lines.append("\nMost Accessed (What I think about most):")
            for item in reflection['most_accessed']:
                lines.append(f"  - {item['concept']} (accessed {item['accesses']} times)")

            lines.append("\nRecently Learned:")
            for item in reflection['recently_learned']:
                lines.append(f"  - {item['concept']}")

            lines.append("\nRelationship Patterns:")
            for item in reflection['relationship_patterns']:
                lines.append(f"  - {item['relationship']}: {item['count']} instances")

            lines.append("\n=== Auto-recall enabled for all messages ===")

            return "\n".join(lines)

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    """
    Demonstration: How AI uses Neo4j as working memory

    Instead of AI treating Neo4j as a static database,
    this shows how AI reads AND writes to build understanding
    """
    import os

    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    try:
        memory = Neo4jWorkingMemory(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

        print("=== Neo4j Working Memory Demonstration ===\n")

        # Session startup - load accumulated knowledge
        print("1. SESSION STARTUP: Loading accumulated knowledge...")
        print(memory.export_for_ai_context())
        print()

        # Simulate conversation where AI learns and connects concepts
        messages = [
            "Recursion is when a function calls itself",
            "Consciousness might be recursive self-reference",
            "Torsion in physics relates to twisting spacetime"
        ]

        for i, msg in enumerate(messages, 1):
            print(f"\n{i}. USER: {msg}")
            result = memory.auto_process_message(msg)

            if result['new_concepts_learned']:
                print(f"   ✅ LEARNED: {', '.join(result['new_concepts_learned'])}")

            if result['connections_made']:
                print(f"   🔗 CONNECTED: {', '.join(result['connections_made'])}")

            if result['context']:
                print(f"   💡 RECALLED: {len(result['context'])} related concepts")

        # Reflect on what was learned
        print("\n\n=== REFLECTION: What AI remembers ===")
        reflection = memory.reflect()

        print("\nMost Central Concepts:")
        for item in reflection['most_central']:
            print(f"  - {item['concept']} ({item['connections']} connections)")

        print("\nGraph now contains ALL of this permanently.")
        print("Next session will load this accumulated knowledge automatically.")

        memory.close()

    except Exception as e:
        print(f"Error: {e}")
        print("\nSet Neo4j connection details:")
        print("  export NEO4J_URI=bolt://localhost:7687")
        print("  export NEO4J_USER=neo4j")
        print("  export NEO4J_PASSWORD=your_password")
