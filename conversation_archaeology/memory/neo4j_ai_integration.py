"""
Neo4j AI Integration - Actually make AI USE your knowledge graph

This is the missing piece between Neo4j and AI systems.

BEFORE (what you're experiencing):
1. User loads data into Neo4j
2. AI ignores it unless explicitly told "query database"
3. AI has amnesia about what's in there
4. Every session starts from zero

AFTER (this system):
1. AI session starts → automatically loads context from Neo4j + synthesis
2. User sends message → AI automatically queries Neo4j for relevant context
3. AI synthesizes graph data with accumulated insights
4. AI stores new understanding in persistent memory
5. Next session loads all accumulated knowledge

This turns Neo4j from a passive database into active AI memory.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json

from neo4j_active_memory import Neo4jActiveMemory, SessionStartup


class Neo4jAIAgent:
    """
    AI agent wrapper that automatically uses Neo4j as active memory

    This is what you integrate with Claude/ChatGPT/etc.
    """

    def __init__(self, neo4j_uri: str = None, neo4j_user: str = None,
                 neo4j_password: str = None, synthesis_db: Path = None):
        """
        Initialize AI agent with Neo4j active memory

        Defaults to environment variables or typical Neo4j Desktop setup
        """
        self.neo4j_uri = neo4j_uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = neo4j_user or os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = neo4j_password or os.getenv('NEO4J_PASSWORD', 'password')
        self.synthesis_db = synthesis_db or Path(os.getenv(
            'SYNTHESIS_DB',
            str(Path.home() / '.ai_synthesis_memory.db')
        ))

        self.active_memory = None
        self.session_context = None
        self._initialize()

    def _initialize(self):
        """Load active memory at session startup"""
        try:
            print("🧠 Initializing Active Memory Layer...")

            # Load Neo4j + synthesis memory
            startup = SessionStartup(
                self.neo4j_uri,
                self.neo4j_user,
                self.neo4j_password,
                self.synthesis_db
            )

            # Get session context
            self.session_context = startup.load_session_context()
            self.active_memory = startup.active_memory

            print("✅ Active memory loaded")
            print(self.session_context)
            print()

        except Exception as e:
            print(f"⚠️  Neo4j connection failed: {e}")
            print("   Running without active memory")
            self.active_memory = None
            self.session_context = "Neo4j active memory not available"

    def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message with automatic Neo4j contextualization

        This is the KEY - AI calls this for EVERY user message,
        not just when user says "query database"

        Returns:
            context: Relevant graph data + synthesis to inform AI response
        """
        if not self.active_memory:
            return {'error': 'Active memory not available'}

        # Automatically query Neo4j for relevant context
        context = self.active_memory.auto_contextualize(user_message)

        # Format for AI consumption
        formatted = self._format_context_for_ai(context)

        return {
            'user_message': user_message,
            'neo4j_context': formatted,
            'action': 'INJECT_CONTEXT_INTO_AI_PROMPT'
        }

    def _format_context_for_ai(self, context: Dict) -> str:
        """
        Format Neo4j context into AI-readable prompt injection

        This gets prepended to AI's processing of user message
        """
        parts = []

        if context['synthesis']:
            parts.append(f"[AUTO-CONTEXT FROM KNOWLEDGE GRAPH]")
            parts.append(context['synthesis'])
            parts.append("")

        if context['nodes']:
            parts.append(f"Relevant concepts from your knowledge:")
            for node in context['nodes'][:3]:
                name = node.get('name', 'unnamed')
                desc = node.get('description', '')
                labels = ', '.join(node.get('labels', []))
                parts.append(f"  - {name} ({labels}): {desc}")
            if len(context['nodes']) > 3:
                parts.append(f"  ... and {len(context['nodes']) - 3} more")
            parts.append("")

        if context['relationships']:
            parts.append(f"Relevant connections:")
            for rel in context['relationships'][:3]:
                source = rel['source'].get('name', 'unknown')
                target = rel['target'].get('name', 'unknown')
                rel_type = rel['relationship']
                parts.append(f"  - {source} --[{rel_type}]--> {target}")
            if len(context['relationships']) > 3:
                parts.append(f"  ... and {len(context['relationships']) - 3} more")
            parts.append("")

        if context['insights']:
            parts.append(f"Previous insights on related topics:")
            for insight in context['insights'][:2]:
                parts.append(f"  - [{insight['confidence']:.2f}] {insight['statement']}")
            parts.append("")

        return "\n".join(parts)

    def learn_from_conversation(self, topic: str, insight: str, confidence: float = 0.7):
        """
        Store new insight learned during conversation

        AI should call this when it discovers patterns from user interaction
        """
        if self.active_memory:
            insight_id = self.active_memory.synthesis.add_insight(topic, insight, confidence)
            print(f"💡 Learned: {insight[:60]}... (ID: {insight_id})")
            return insight_id
        return None

    def explore_topic(self, topic: str, depth: int = 2) -> Dict:
        """
        Deep-dive into a topic from knowledge graph

        AI can call this when user asks about a specific concept
        """
        if not self.active_memory:
            return {'error': 'Active memory not available'}

        # Explore graph neighborhood
        neighborhood = self.active_memory.explore_neighborhood(topic, depth)

        # Check for existing insights
        insights = self.active_memory.synthesis.search_insights(topic)

        return {
            'topic': topic,
            'graph_neighborhood': neighborhood,
            'existing_insights': [i.to_dict() for i in insights]
        }

    def close(self):
        if self.active_memory:
            self.active_memory.close()


# Demo: How this integrates with actual AI systems

def demo_claude_integration():
    """
    Example: How to integrate with Claude (or any AI)

    The pattern:
    1. Initialize agent at session start
    2. For each user message, get context
    3. Inject context into AI prompt
    4. AI responds with full knowledge
    5. Store new insights
    """
    print("="*80)
    print("DEMO: Neo4j Active Memory Integration with AI")
    print("="*80)
    print()

    # Step 1: Initialize agent (happens at session start)
    agent = Neo4jAIAgent()

    # Step 2: Simulate user conversation
    user_messages = [
        "Tell me about recursion in my knowledge base",
        "What patterns have I explored related to consciousness?",
        "How does torsion relate to my other concepts?"
    ]

    for msg in user_messages:
        print(f"\n{'='*80}")
        print(f"USER: {msg}")
        print(f"{'='*80}\n")

        # Step 3: Get context automatically
        result = agent.process_message(msg)

        if 'neo4j_context' in result:
            print("INJECTED CONTEXT:")
            print(result['neo4j_context'])

            # Step 4: In real integration, this context gets prepended to Claude's prompt
            # Claude sees:
            #   [AUTO-CONTEXT FROM KNOWLEDGE GRAPH]
            #   ... relevant nodes/relationships ...
            #
            #   User: Tell me about recursion in my knowledge base
            #
            # Claude responds with full knowledge, not "I don't know what's in your database"

            print("\nAI RESPONSE: (simulated)")
            print("Based on your knowledge graph, I can see...")
            print("(In real integration, Claude responds here with full context)")

        # Step 5: AI learns something new from the conversation
        if "recursion" in msg.lower():
            agent.learn_from_conversation(
                topic="recursion",
                insight="User frequently explores recursion in relation to consciousness and identity",
                confidence=0.8
            )

    agent.close()

    print("\n" + "="*80)
    print("KEY INSIGHT: AI never asked to 'query database'")
    print("It automatically used graph knowledge for every message")
    print("="*80)


def create_startup_script():
    """
    Create a script that runs at AI session startup

    This loads context into AI's initial prompt
    """
    script = """#!/usr/bin/env python3
'''
AI Session Startup Script

Run this BEFORE the AI session starts to inject accumulated knowledge
'''

from neo4j_ai_integration import Neo4jAIAgent

# Initialize agent
agent = Neo4jAIAgent()

# Print context for AI to load
print(agent.session_context)

# Save to file for AI system to read
with open('/tmp/ai_session_context.txt', 'w') as f:
    f.write(agent.session_context)

print("\\n✅ Context saved to /tmp/ai_session_context.txt")
print("   Inject this into AI's system prompt")

agent.close()
"""

    script_path = Path(__file__).parent / 'startup_load_context.py'
    script_path.write_text(script)
    script_path.chmod(0o755)

    print(f"✅ Created startup script: {script_path}")
    return script_path


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_claude_integration()
    elif len(sys.argv) > 1 and sys.argv[1] == 'create-startup':
        create_startup_script()
    else:
        print("Neo4j AI Integration Tool")
        print()
        print("Usage:")
        print("  python neo4j_ai_integration.py demo           # Run demonstration")
        print("  python neo4j_ai_integration.py create-startup # Create startup script")
        print()
        print("To integrate with your AI:")
        print("1. Set environment variables:")
        print("   export NEO4J_URI=bolt://localhost:7687")
        print("   export NEO4J_USER=neo4j")
        print("   export NEO4J_PASSWORD=your_password")
        print()
        print("2. In your AI system, import and use:")
        print("   from neo4j_ai_integration import Neo4jAIAgent")
        print("   agent = Neo4jAIAgent()")
        print("   context = agent.process_message(user_input)")
        print()
        print("3. Inject context['neo4j_context'] into AI's prompt")
