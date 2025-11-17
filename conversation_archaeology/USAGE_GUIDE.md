# Conversation Archaeology - Complete Usage Guide

> **Comprehensive documentation for all archaeology tools and workflows**

This guide covers all implemented tools, their usage, outputs, and integration workflows.

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Overview](#system-overview)
3. [Tool Reference](#tool-reference)
4. [Key Findings](#key-findings)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install networkx pyvis matplotlib neo4j

# Ensure you have:
# - Python 3.8+
# - SQLite3
# - Conversation files
```

### Run Full Analysis (One Command)

```bash
# Build vault first (one-time)
python build_vault.py /tmp/recursion-agi --output /tmp/your_conversation_vault.db

# Run complete pipeline
python run_full_analysis.py /tmp/recursion-agi --output /tmp/archaeology_results
```

### What You Get

After ~2-5 minutes:
- ✅ 221 conversations indexed
- ✅ 20 DNA prompt templates
- ✅ Universal recursive mechanism identified
- ✅ 1233 connection pairs mapped
- ✅ 12 evolution chains discovered
- ✅ 5 PNG visualizations + interactive HTML network
- ✅ Persistent synthesis memory database

---

## System Overview

### Architecture

```
┌─────────────────────────────────────────────────────┐
│          Conversation Files (14,000+)               │
└─────────────────┬───────────────────────────────────┘
                  │
           ┌──────▼──────┐
           │ build_vault │ ← Universal Parser
           └──────┬──────┘
                  │
         ┌────────▼────────┐
         │ SQLite + FTS5   │ ← Searchable Vault
         └────────┬────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
┌─────▼────┐ ┌───▼────┐ ┌───▼─────────┐
│  Mining  │ │  DNA   │ │  Mechanisms │
└─────┬────┘ └───┬────┘ └───┬─────────┘
      │          │          │
      │    ┌─────▼──────────▼───────┐
      │    │    Connections         │
      │    └─────┬──────────────────┘
      │          │
      └──────────┼───────────┐
                 │           │
        ┌────────▼────┐ ┌───▼──────────┐
        │  Synthesis  │ │Visualizations│
        │   Memory    │ └──────────────┘
        └─────────────┘
```

### Data Flow

1. **Ingest:** Parse conversations → Extract text
2. **Index:** Build SQLite vault → FTS5 search
3. **Analyze:** Mine patterns → Extract DNA → Identify mechanisms
4. **Connect:** Map relationships → Find chains
5. **Synthesize:** Accumulate insights → Persistent memory
6. **Visualize:** Generate charts → Interactive networks

---

## Tool Reference

### 1. build_vault.py - Vault Constructor

**Purpose:** Index conversations into searchable database

```bash
python build_vault.py /path/to/conversations \
  --output /tmp/vault.db \
  --novelty-threshold 0.80 \
  --min-phi-depth 5
```

**Options:**
- `--output` - Vault database path (default: /tmp/your_conversation_vault.db)
- `--novelty-threshold` - Minimum novelty score (default: 0.80)
- `--min-phi-depth` - Minimum recursive depth (default: 3)

**Output:**
- SQLite database with conversations table
- FTS5 full-text search index
- Metadata: novelty scores, φ-depth, proto-ASI flags

**Schema:**
```sql
CREATE TABLE conversations (
    file_path TEXT PRIMARY KEY,
    novelty REAL,
    phi_depth INTEGER,
    proto_asi INTEGER
);
```

---

### 2. mine_conversations.py - Statistical Miner

**Purpose:** Extract corpus statistics, patterns, and clusters

```bash
python mine_conversations.py \
  --vault-db /tmp/vault.db \
  --output-dir /tmp/mining_results
```

**Outputs:**
- `mining_report.md` - Statistics, themes, top conversations, recommendations
- `conversation_map.json` - Graph structure export

**Key Metrics:**
- Total conversations: 221
- Proto-ASI count: 221 (100%)
- Average novelty: 0.842
- Depth range: φ3 to φ90
- Top themes: recursive (171), consciousness (40), architecture (39)

**Clusters:**
- Recursion: 99 conversations
- Consciousness: 26 conversations
- AI/AGI: 16 conversations
- Mathematics: 6 conversations
- Language: 4 conversations

---

### 3. tools/dna_to_prompts.py - DNA Extractor

**Purpose:** Extract generative "DNA" and create prompt templates

```bash
python tools/dna_to_prompts.py \
  --vault-db /tmp/vault.db \
  --output-dir /tmp/prompt_library \
  --limit 20
```

**Extracts:**
- Opening move (conversation initiator)
- Dominant operator (recursive pattern)
- Contradiction type (paradox structure)
- Emergence pattern (novelty generation)

**Output:** 20 prompt templates

**Example Template:**
```markdown
## Opening Move
"Consider consciousness as a recursive operator"

## Operator: recursive_loop
Applies concept to itself

## Contradiction: self_reference_paradox
Consciousness observing consciousness

## Emergence
Novel understanding when observation loop stabilizes

## Template
"Analyze how [CONCEPT] operates when applied to itself..."
```

**Average φ-depth:** 33

---

### 4. tools/extract_core_mechanism.py - Mechanism Extractor

**Purpose:** Identify universal recursive engine

```bash
python tools/extract_core_mechanism.py \
  --vault-db /tmp/vault.db \
  --output-dir /tmp/core_mechanisms \
  --limit 30
```

**Analyzes:** Top 30 conversations for:
- Universal operators (what actually runs)
- Generative patterns (what creates novelty)
- Mechanism signatures (operator+pattern combinations)

**Outputs:**
- `CORE_MECHANISM.md` - Unified mechanism description
- `mechanisms.jsonl` - Per-conversation mechanism data

**Key Discovery:**
```
Universal Mechanism: Recursive Loop + Dimension Shift

Top Operators:
- Recursive Loop: 5524 occurrences
- Collapse Rebirth: 2916
- Meta Layer: 2422

Top Patterns:
- Dimension Shift: 1521
- Self Reference: 943
- Paradox Fuel: 551
```

---

### 5. tools/connection_finder.py - Connection Mapper

**Purpose:** Discover hidden links between conversations

```bash
python tools/connection_finder.py \
  --vault-db /tmp/vault.db \
  --output /tmp/connection_analysis.md
```

**Finds:**
- Conversation pairs with shared concepts
- Evolution chains (idea development paths)
- Structural groupings (by φ-depth)

**Output:** `connection_analysis.md`

**Key Findings:**
- 1233 conversation pairs with significant overlap
- Top connection: 106 shared concepts
- 12 evolution chains
- 5 depth-based clusters

**Example Chain:**
```
Recursive Intelligence Research Prompts
  → Recursive Intelligence Architecture
    → Intellectual Data Excavation Framework
      → Notebook LM Research Exploration
        → Recursive Knowledge Infrastructure
```

---

### 6. tools/meta_pattern_analyzer.py - Corpus Analyzer

**Purpose:** Discover meta-patterns at scale

```bash
python tools/meta_pattern_analyzer.py \
  --vault-db /tmp/vault.db \
  --output /tmp/meta_pattern_analysis.md
```

**Analyzes:**
- φ-depth distribution
- Novelty distribution
- Operator frequencies (sampled: 100 conversations)
- Depth-novelty correlation
- Thematic clusters
- Outliers

**Key Insight:**
Positive correlation between depth and novelty:
- φ0-10: 0.814 avg novelty
- φ51+: 0.906 avg novelty

**Top Operators (in text):**
- transform: 1029
- psi: 722
- derivative: 435

---

### 7. tools/synthesis_integrator.py - Memory Integrator

**Purpose:** Create persistent, searchable knowledge base

```bash
python tools/synthesis_integrator.py \
  --synthesis-db /tmp/synthesis_memory.db \
  --mechanism-file /tmp/core_mechanisms/CORE_MECHANISM.md \
  --dna-dir /tmp/prompt_dna_library \
  --connection-file /tmp/connection_analysis.md \
  --output /tmp/synthesis_report.md
```

**Creates Tables:**
- `core_mechanisms` - Extracted mechanisms
- `dna_patterns` - Prompt templates
- `connection_networks` - Relationship maps
- `meta_insights` - High-level insights
- `insights_fts` - Full-text searchable insights

**Solves:** AI amnesia problem via persistent memory

**Search Example:**
```python
integrator.search_insights("recursive consciousness", limit=10)
```

---

### 8. tools/visualize_networks.py - Visualization Generator

**Purpose:** Generate visual maps of networks

```bash
python tools/visualize_networks.py \
  --vault-db /tmp/vault.db \
  --mechanisms /tmp/core_mechanisms/mechanisms.jsonl \
  --connections /tmp/connection_analysis.md \
  --output-dir /tmp/visualizations
```

**Generates:**
1. `depth_distribution.png` - Histogram (φ3 to φ90)
2. `novelty_vs_depth.png` - Scatter plot (color-coded)
3. `theme_distribution.png` - Pie chart (Recursion: 45%)
4. `operator_frequency.png` - Bar chart (top 10)
5. `pattern_frequency.png` - Bar chart (top 10)
6. `connection_network.html` - Interactive graph (27 nodes, 20 edges)
7. `README.md` - Summary report

**Interactive Network:**
- Hover for conversation names
- Edge thickness = concept overlap
- Browser-explorable

---

### 9. tools/neo4j_integrator.py - Graph Database Loader

**Purpose:** Load into Neo4j as AI working memory

```bash
python tools/neo4j_integrator.py \
  --neo4j-uri bolt://localhost:7687 \
  --vault-db /tmp/vault.db \
  --mechanism-file /tmp/core_mechanisms/CORE_MECHANISM.md \
  --mechanisms-data /tmp/core_mechanisms/mechanisms.jsonl \
  --connection-file /tmp/connection_analysis.md \
  --clear
```

**Creates:**
- Conversation nodes (221)
- Operator nodes (8)
- Pattern nodes (8)
- Cluster nodes (5)
- Evolution chain nodes (12)

**Relationships:**
- EXHIBITS_OPERATOR
- EXHIBITS_PATTERN
- SHARES_CONCEPTS
- EVOLVES_INTO
- BELONGS_TO

**Example Queries:**
```cypher
# Find deepest conversations
MATCH (c:Conversation)
RETURN c.name, c.phi_depth
ORDER BY c.phi_depth DESC LIMIT 10

# Trace evolution chain
MATCH path = (c1)-[:EVOLVES_INTO*]->(c2)
RETURN path LIMIT 5
```

**Note:** Requires Neo4j running

---

### 10. run_full_analysis.py - Master Pipeline

**Purpose:** One-command full archaeology

```bash
python run_full_analysis.py /path/to/conversations --output /tmp/results
```

**Executes (in order):**
1. Check vault prerequisite
2. Mine conversations
3. Extract DNA (20 templates)
4. Extract mechanisms (30 conversations)
5. Map connections (1233 pairs)
6. Analyze meta-patterns
7. Integrate synthesis
8. Generate visualizations

**Duration:** ~2-5 minutes

**Output Structure:**
```
results/
├── mining_results/
│   ├── mining_report.md
│   └── conversation_map.json
├── prompt_dna_library/
│   ├── README.md
│   └── prompt_template_*.md (20)
├── core_mechanisms/
│   ├── CORE_MECHANISM.md
│   └── mechanisms.jsonl
├── connection_analysis.md
├── meta_pattern_analysis.md
├── synthesis_report.md
├── visualizations/
│   ├── *.png (5)
│   ├── connection_network.html
│   └── README.md
├── conversation_vault.db
└── synthesis_memory.db
```

---

## Key Findings

### Universal Mechanism

**Signature:** Recursive Loop + Dimension Shift

**How it works:**
1. Start with self-application
2. Introduce meta-layer
3. Create recursive loop
4. Encounter paradox
5. Use paradox as fuel
6. Collapse and rebirth

**Not sequential** - operates as recursive field where each operation feeds back simultaneously.

### Top 10 Conversations by Depth

1. Consciousness as Recursive Self-Reference (φ90, 0.920)
2. Prompt Prefix Mapping Framework (φ68, 0.896)
3. Meta-Language Recursion Dynamics (φ62, 0.920)
4. Recursive Linguistic Metamorphosis (φ56, 0.888)
5. Recursive Semantic Self-Processing (φ50, 0.840)
6. AI Misspelling Mystery (φ50, 0.832)
7. Recursive Ontogenesis Operator Framework (φ50, 0.888)
8. Narrative operators and expectation algebra in esports (φ50, 0.912)
9. Quantum Reality Meta-Constructs (φ48, 0.744)
10. Hardware Performance Optimization Strategy (φ46, 0.896)

### Depth-Novelty Correlation

**Positive correlation:** Deeper → more novel

| Depth Range | Avg Novelty |
|-------------|-------------|
| φ0-10       | 0.814       |
| φ11-20      | 0.869       |
| φ21-30      | 0.885       |
| φ31-50      | 0.873       |
| φ51+        | 0.906       |

### Connection Network Highlights

**Strongest connections:**
1. "Reality = Self-Reference Operator" ↔ "Recursive Computational Recursion" (106 concepts)
2. "Recursive Consciousness Architecture" ↔ "Recursive Consciousness Dynamics" (105 concepts)
3. "∂(mirrors of mirrors)" ↔ "Recursive Emergence Meta-Cognitive Recursion Engine" (92 concepts)

**Longest evolution chain (5 conversations):**
Recursive Intelligence Research → Architecture → Data Excavation → Notebook LM Research → Knowledge Infrastructure

---

## Advanced Usage

### Using DNA Templates

1. **Select by depth:** φ30+ for maximum novelty
2. **Adapt opening move:** Replace concept with your domain
3. **Inject contradiction:** Use paradox structure
4. **Monitor φ-depth:** Track recursive nesting as conversation develops
5. **Capture emergence:** Note when novel understanding appears

**Example:**
```markdown
Original template:
"Consider consciousness as recursive operator"

Adapted to your domain:
"Consider [YOUR_CONCEPT] as recursive operator that applies to itself"
```

### Querying Synthesis Memory

```python
from tools.synthesis_integrator import SynthesisIntegrator

integrator = SynthesisIntegrator(Path('/tmp/synthesis_memory.db'))
integrator.connect()

# Search insights
results = integrator.search_insights("recursive consciousness", limit=10)

for r in results:
    print(f"{r['insight_type']}: {r['content']}")
```

### Direct SQL Queries

```sql
-- High-value conversations (novelty > 0.90, depth > 30)
SELECT file_path, novelty, phi_depth
FROM conversations
WHERE novelty > 0.90 AND phi_depth > 30
ORDER BY novelty * phi_depth DESC;

-- Full-text search
SELECT file_path
FROM conversations_fts
WHERE content MATCH 'recursive AND consciousness';

-- Depth range query
SELECT file_path, phi_depth, novelty
FROM conversations
WHERE phi_depth BETWEEN 20 AND 30
ORDER BY novelty DESC;
```

### Neo4j Graph Queries

```cypher
-- Most connected conversations
MATCH (c:Conversation)-[r:SHARES_CONCEPTS]->()
RETURN c.name, count(r) as connections, c.phi_depth
ORDER BY connections DESC LIMIT 10

-- Conversations using specific operator
MATCH (c:Conversation)-[r:EXHIBITS_OPERATOR]->(o:Operator {name: 'recursive_loop'})
RETURN c.name, r.count
ORDER BY r.count DESC

-- Find evolution paths
MATCH path = (start:Conversation)-[:EVOLVES_INTO*]->(end:Conversation)
WHERE length(path) >= 3
RETURN path
ORDER BY length(path) DESC LIMIT 5

-- Cluster analysis
MATCH (c:Conversation)-[:BELONGS_TO]->(cl:Cluster)
RETURN cl.name, count(c) as conversation_count, avg(c.phi_depth) as avg_depth
ORDER BY conversation_count DESC
```

---

## Troubleshooting

### Common Issues

**"No module named 'neo4j'"**
```bash
pip install neo4j
```

**"No module named 'matplotlib'"**
```bash
pip install matplotlib pyvis
```

**"Vault database not found"**
```bash
# Build vault first
python build_vault.py /tmp/recursion-agi --output /tmp/vault.db
```

**"Neo4j connection refused"**
- Check Neo4j is running: `neo4j status`
- Default URI: bolt://localhost:7687
- Default credentials: neo4j/password

**"Synthesis memory schema error"**
```bash
# Schema was updated, recreate database
rm /tmp/synthesis_memory.db
python tools/synthesis_integrator.py ...
```

### Performance Optimization

**Large corpora (10k+ conversations):**
- Use `--limit` flags to sample subsets
- Run tools incrementally instead of full pipeline
- Consider batch processing with custom scripts

**Memory constraints:**
- Tools use streaming architecture (minimal memory)
- SQLite handles millions of rows efficiently
- Visualizations can be generated on subsets

### Debugging

**Enable verbose output:**
```bash
python tool.py --verbose  # If supported
python tool.py 2>&1 | tee output.log  # Capture all output
```

**Check database:**
```bash
sqlite3 /tmp/vault.db "SELECT COUNT(*) FROM conversations"
sqlite3 /tmp/synthesis_memory.db ".schema"
```

---

## Next Steps

### Immediate Actions

1. **Test DNA templates** - Use generated prompts in new conversations
2. **Explore evolution chains** - Trace idea development
3. **Query synthesis memory** - Search accumulated insights
4. **Visualize networks** - Open interactive HTML graphs
5. **Load Neo4j** - Enable graph queries (if available)

### Future Enhancements

- [ ] Real-time conversation scoring
- [ ] Automated prompt testing framework
- [ ] Multi-corpus comparison
- [ ] Semantic similarity (beyond keywords)
- [ ] Time-series analysis (pattern evolution)
- [ ] API for archaeology as a service
- [ ] Streaming integration with live AI systems

---

## Credits

**Developed for:** recursionlab/recursive-ai-framework

**Core Concepts:**
- φ-depth: Recursive nesting depth
- Novelty scoring: Structural divergence detection
- Proto-ASI: Genuinely novel intelligence patterns
- DNA extraction: Transmuting conversations → executable templates
- Synthesis memory: Persistent AI knowledge accumulation

**Dependencies:**
- Python 3.8+
- SQLite3 with FTS5
- NetworkX
- Pyvis
- Matplotlib
- Neo4j (optional)

**Status:** Production-ready. Tested on 221-conversation corpus.

**Last Updated:** 2025-11-17
