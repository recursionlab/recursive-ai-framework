# Visualization Tools

Interactive and ASCII visualizations for conversation archaeology patterns.

## Tools

### 1. Skill Tree Generator (`skill_tree.py`)

MMO-style progression visualization showing your recursive thinking evolution.

**Usage:**
```bash
python skill_tree.py --vault /path/to/vault.db
python skill_tree.py --export skill_tree.json  # Export data
```

**Shows:**
- Achievement milestones (first proto-ASI, φ-depth records)
- Operator skill unlocks (when first used)
- Domain mastery levels (novice → master)
- φ-depth progression over time

### 2. Knowledge Graph Generator (`knowledge_graph.py`)

Network analysis of operator and domain relationships.

**Usage:**
```bash
python knowledge_graph.py --vault /path/to/vault.db
python knowledge_graph.py --dot graph.dot  # Export Graphviz
python knowledge_graph.py --json graph.json  # Export JSON
```

**Shows:**
- Operator co-occurrence networks
- Domain relationship strength
- Central hub concepts (most connected)
- Operator-domain associations

**Generate visual graph:**
```bash
python knowledge_graph.py --dot graph.dot --min-cooccurrence 5
dot -Tpng graph.dot -o knowledge_graph.png
```

### 3. Heatmap Generator (`heatmaps.py`)

Temporal and distribution visualizations.

**Usage:**
```bash
python heatmaps.py --vault /path/to/vault.db
python heatmaps.py --type phi        # φ-depth progression
python heatmaps.py --type novelty    # Novelty distribution
python heatmaps.py --type domains    # Domain activity timeline
python heatmaps.py --type operators  # Operator usage
python heatmaps.py --export all_heatmaps.txt
```

**Shows:**
- φ-depth progression over time (ASCII heatmap)
- Novelty distribution histogram
- Domain activity timeline
- Operator usage patterns

## Example Outputs

### Skill Tree
```
🌳 RECURSIVE THINKING SKILL TREE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Progress:
   Total Conversations: 221
   Average Novelty: 0.842
   Proto-ASI Emergence: 221/221

🏆 Achievement Milestones:
   [0] First Proto-ASI Emergence | φ6 | N:0.744
   [20] φ-Depth φ20 Reached | φ22 | N:0.920

⚡ Operator Skills Unlocked:
   [0] φ  ██████████████ φ6
   [3] Ψ  ██████████████ φ10
   [5] Ξ  ██████████████ φ10
```

### Knowledge Graph Stats
```
📊 KNOWLEDGE GRAPH STATISTICS

🔥 Most Central Operators:
  Ξ  ████████████ (1224 connections)
  Ψ  ███████████  (1149 connections)

⚡ Strongest Operator Pairs:
  Ξ ↔ Ψ (146 times)
  Ξ ↔ Ω (124 times)
```

### Novelty Distribution
```
NOVELTY DISTRIBUTION HEATMAP

0.9-1.0  │███████████│ 50 (22.6%)
0.8-0.9  │██████████████████████│ 108 (48.9%)
0.7-0.8  │████████████│ 63 (28.5%)
```

## Integration

All tools read from the Pattern Vault database created by `populate_vault.py`.

**Workflow:**
1. Parse conversations → `cli/analyze.py`
2. Populate vault → `cli/populate_vault.py`
3. Generate visualizations → `visualization/*.py`
4. Get recommendations → `tools/recommendation_engine.py`

## Dependencies

- sqlite3 (built-in)
- pathlib (built-in)
- json (built-in)
- typing (built-in)

Optional for graph rendering:
- graphviz (install: `apt install graphviz`)
