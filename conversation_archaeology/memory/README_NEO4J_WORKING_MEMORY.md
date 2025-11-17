# Neo4j as AI Working Memory

## The Problem You Had

You loaded data into Neo4j, but AI only used it when explicitly told to "query the database". Every session started with amnesia. The graph was passive storage, not active memory.

## The Solution

This system makes Neo4j the AI's **working memory** - it reads AND writes to build understanding over time.

## How It Works

### 1. Session Startup
```python
from neo4j_working_memory import Neo4jWorkingMemory

# AI loads accumulated knowledge at session start
memory = Neo4jWorkingMemory(uri, user, password)
context = memory.export_for_ai_context()

# This context gets injected into AI's initial prompt
# AI now knows everything it's learned previously
```

### 2. Every User Message
```python
# AI automatically processes message with working memory
result = memory.auto_process_message(user_message)

# AI gets:
# - Relevant context from graph
# - New concepts detected and stored
# - Connections made between concepts
```

### 3. AI Learns Something New
```python
# When AI realizes a new concept, it writes to graph
memory.remember(
    concept="Recursion",
    properties={
        'description': "When a function calls itself",
        'confidence': 0.9
    },
    labels=['Programming', 'MathConcept']
)
```

### 4. AI Makes Connections
```python
# When AI sees relationship between concepts
memory.connect(
    from_concept="Recursion",
    to_concept="Consciousness",
    relationship="MIGHT_EXPLAIN",
    properties={'strength': 0.7}
)
```

### 5. Understanding Deepens
```python
# When AI learns more about existing concept
memory.deepen(
    concept="Recursion",
    new_understanding={
        'examples': "factorial, fibonacci, tree traversal",
        'confidence': 0.95  # increased confidence
    }
)
```

### 6. Next Session
AI loads all accumulated knowledge and continues building from where it left off. No amnesia.

## Key Methods

### `remember(concept, properties, labels)` → Write New Knowledge
Store new concept in graph with properties and labels.

### `connect(from, to, relationship, properties)` → Link Concepts
Create relationship between concepts (builds the graph structure).

### `deepen(concept, new_understanding)` → Update Knowledge
Update/add properties to existing concept.

### `recall(query)` → Retrieve Context
Search graph for relevant concepts (called automatically).

### `reflect()` → Discover Patterns
Analyze graph to find central concepts, patterns, frequently accessed nodes.

### `auto_process_message(message)` → Automatic Integration
Process user message: recall context, detect new concepts, make connections.

## Integration with Your AI

### Option 1: Manual Integration (any AI)

```python
from neo4j_working_memory import Neo4jWorkingMemory
import os

# Setup
memory = Neo4jWorkingMemory(
    uri=os.getenv('NEO4J_URI'),
    user=os.getenv('NEO4J_USER'),
    password=os.getenv('NEO4J_PASSWORD')
)

# Session start
initial_context = memory.export_for_ai_context()
# Inject initial_context into AI's system prompt

# For each user message
def process_with_memory(user_message):
    # Get context automatically
    result = memory.auto_process_message(user_message)

    # Format context for AI
    context_str = f"""
[WORKING MEMORY CONTEXT]
Relevant concepts: {[c['name'] for c in result['context']]}
New learnings: {result['new_concepts_learned']}
Connections made: {result['connections_made']}
    """

    # Send to AI with context prepended
    full_prompt = context_str + "\n\nUser: " + user_message
    ai_response = your_ai_api_call(full_prompt)

    return ai_response
```

### Option 2: Programmatic Learning

When AI explicitly learns something:

```python
# AI's internal process:
# "User just taught me that recursion relates to consciousness"

memory.remember("Recursion", {
    'description': "Self-referential function calls",
    'domain': "programming"
})

memory.remember("Consciousness", {
    'description': "Self-aware awareness",
    'domain': "philosophy"
})

memory.connect(
    "Recursion",
    "Consciousness",
    "MIGHT_EXPLAIN",
    properties={
        'hypothesis': "Consciousness is recursive self-reference",
        'confidence': 0.6
    }
)
```

## Comparison: Before vs After

### Before (What You Had)
```
User: "Tell me about recursion in my notes"
AI: "I don't know what's in your database. Would you like me to query it?"
User: "Yes, query the database"
AI: [queries] "Found 15 notes about recursion. Here they are..."
User: "How does recursion relate to consciousness?"
AI: "I don't have access to that information"
```

**Problem:** AI treats graph as external storage. No accumulated understanding.

### After (Working Memory)
```
[Session starts]
AI loads: "Working memory contains 347 concepts, most central: Recursion (45 connections)"

User: "Tell me about recursion in my notes"
AI: [auto-recalls from graph] "Based on your knowledge graph, you've explored recursion across 3 domains: programming (fibonacci, factorials), mathematics (induction, proof), and consciousness (self-reference paradoxes). Your most developed insight is the connection between recursive self-reference and awareness..."

User: "Actually, I think recursion might explain time loops"
AI: [creates new concept "time loops", connects to "recursion" with relationship "EXPLAINED_BY"]
    "Interesting - I've stored that connection. This relates to your existing concepts about causality and temporal paradoxes. Should we explore how this fits with your work on..."
```

**Result:** AI uses graph as working memory. Understands your knowledge. Builds on it.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install neo4j
```

### 2. Configure Neo4j Connection
```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
```

### 3. Test the System
```bash
python neo4j_working_memory.py
```

You should see:
- Session loading accumulated knowledge
- AI processing messages and learning
- Concepts being stored and connected
- Reflection showing what was learned

### 4. Integrate with Your AI

See "Integration with Your AI" section above.

## Files

- `neo4j_working_memory.py` - Core working memory implementation
- `neo4j_active_memory.py` - Additional utilities for pattern discovery
- `neo4j_ai_integration.py` - Integration examples
- This README

## What This Solves

✅ **Amnesia:** Graph persists all knowledge across sessions
✅ **Passive storage:** AI actively reads AND writes as it learns
✅ **Manual queries:** AI automatically recalls relevant context
✅ **No synthesis:** AI builds understanding by connecting concepts
✅ **Static data:** Graph grows as AI learns from conversations

## Next Steps

1. **Test with simple concepts** - Run the demo, verify it works
2. **Import existing knowledge** - Bulk load your current notes/data
3. **Integrate with AI** - Wire into Claude/ChatGPT/your AI system
4. **Monitor growth** - Use `reflect()` to see what AI is learning
5. **Refine** - Adjust confidence thresholds, relationship types, etc.

## Philosophy

The graph isn't just storage. It's the AI's **memory substrate**.

Just like your brain doesn't "query your hippocampus" - it automatically recalls relevant context when thinking - the AI should automatically use the graph when processing messages.

This makes the graph a living, growing representation of what the AI knows about you and your knowledge.
