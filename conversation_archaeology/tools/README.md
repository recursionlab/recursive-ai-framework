# Analysis Tools

Advanced pattern analysis and recommendation engines.

## Tools

### Recommendation Engine (`recommendation_engine.py`)

Suggests next exploration paths based on your conversation history.

**Usage:**
```bash
python recommendation_engine.py --vault /path/to/vault.db
```

**Provides:**

1. **Underexplored Domains**
   - Identifies domains with low conversation counts
   - Prioritizes high-impact unexplored territory
   - Suggests bridging strategies

2. **Unexplored Operator Combinations**
   - Finds proven operators never paired together
   - Ranks by operator importance
   - Suggests novel synthesis opportunities

3. **φ-Depth Progression Targets**
   - Next milestone depths to reach
   - Gap analysis from current max
   - Difficulty estimates

4. **Thinking Mode Variations**
   - Underused thinking modes
   - Balance recommendations

5. **Synthesis Recommendations**
   - Meta-recursive applications
   - Domain bridging strategies
   - Sustained depth exploration

## Example Output

```
🔮 PATTERN EXPLORATION RECOMMENDATIONS

🎯 Underexplored Domains (High Priority):
  🔥 identity (0 convos) - Opportunity for depth
  🔥 emergence (0 convos) - Opportunity for depth

⚡ Unexplored Operator Combinations:
  • Ξ ⊗ Meta∘Para (Both proven, never paired)
  • φ ⊗ ∇T (Both proven, never paired)

📈 φ-Depth Progression Targets:
  🟡 φ100 (gap: 10 levels) - Next milestone
  🔴 φ150 (gap: 60 levels) - Next milestone

🔬 Synthesis Recommendations:
  1. Bridge recursion with identity
  2. Meta-recursive application of Ξ
  3. Sustained φ-depth exploration
```

## Future Tools

Planned additions:

- **Pattern Refinement Tracker**: Track how patterns evolve across conversations
- **Conversation Lineage Tracer**: Map conversation fork points and continuations
- **Novelty Predictor**: Estimate novelty of new topic combinations
- **Domain Synergy Analyzer**: Find high-value domain intersections

## Integration

Works with Pattern Vault database. Run after vault population:

```bash
# Populate vault
python cli/populate_vault.py ~/conversations/ --vault vault.db

# Get recommendations
python tools/recommendation_engine.py --vault vault.db
```

## Dependencies

- sqlite3 (built-in)
- pathlib (built-in)
- typing (built-in)
- collections (built-in)
