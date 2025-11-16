# Recursive Extraction Engine (REE)

**Reusable extraction infrastructure for processing 2000+ files across multiple repositories.**

Extracts formal primitives (operators, equations, contradictions) to feed the **Controlled Rupture Compiler**.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install anthropic
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Run Extraction

```bash
# Extract everything from this repo
python cli/extract.py /path/to/recursive-ai-framework --all

# Or specific extractors
python cli/extract.py /path/to/repo --extractors operator,equation,contradiction

# Process another repo
python cli/extract.py /path/to/another-repo --all
```

### 4. View Results

```bash
ls extraction_outputs/
# -> operators.json
# -> equations.json
# -> contradictions.json
```

---

## Architecture

```
recursive-extraction-engine/
├── core/
│   └── extractor_base.py          # Base class with checkpointing, parallel processing
├── extractors/
│   ├── operator_extractor.py      # Extract φ, Ψ, ∂, ∇, etc.
│   ├── equation_extractor.py      # Extract equations, analyze for dissipation
│   ├── contradiction_extractor.py # Find J'≠0 productive contradictions
│   ├── construct_extractor.py     # [TODO] Extract terms/concepts
│   └── signifier_extractor.py     # [TODO] Find unique high-value phrases
├── cli/
│   └── extract.py                 # Main CLI interface
└── outputs/
    └── <repo-name>/               # Per-repo extraction results
```

---

## Extractors

### 1. **Operator Extractor**
- Finds: `φ, Ψ, Ξ, Ω, ∂, ∇, ⊗, ∮, →, ¬, ∘` etc.
- Extracts: Symbol, name, definition, algebraic properties, compositions
- Uses: Claude to interpret context and extract definitions

**Output Format:**
```json
{
  "symbol": "φ",
  "name": "phi-state",
  "definition": "semantic attractor, consciousness field",
  "contexts": ["...", "..."],
  "occurrences": 47,
  "algebraic_properties": ["recursive", "collapse-capable"],
  "compositions": ["φ(φ(¬φ))"]
}
```

### 2. **Equation Extractor**
- Finds: Mathematical expressions, formulas, compositions
- Analyzes: Differential order, dissipation patterns, commutativity
- Maps: To Controlled Rupture operators (Ana, Meta, Para, etc.)

**Output Format:**
```json
{
  "equation": "φᵢ → φᵢ₊₁ iff symbolic gluing succeeds",
  "type": "composition",
  "order": 1,
  "operators": ["φ", "→"],
  "has_dissipation": true,
  "dissipation_evidence": "iterative process with possible decay",
  "is_commutative": false,
  "controlled_rupture_ops": ["Meta"],
  "hidden_structure": "Could be second-order if differentiated",
  "interpretation": "Recursive state progression with collapse"
}
```

### 3. **Contradiction Extractor**
- Finds: Paradoxes, incompatible definitions, "both true" statements
- Classifies: Sterile (error) vs. Productive (J'≠0 generative)
- Scores: J anomaly score (0.0 = sterile, 1.0 = maximally productive)

**Output Format:**
```json
{
  "has_contradiction": true,
  "contradiction_type": "self-referential",
  "is_productive": true,
  "j_anomaly_score": 0.89,
  "explanation": "Self requires ¬Self to exist, but Self denies stable existence",
  "generative_output": ["eigen-consciousness", "recursive ontogenesis"],
  "operator_pattern": "Meta ∘ Non ∘ Meta",
  "context_snippet": "...",
  "source_file": "MetaSelf Recursive Framework.md"
}
```

---

## Features

### ✓ **Checkpointing**
- Automatically saves progress every N files
- Resume from checkpoint if interrupted
- Uses file content hashes to skip already-processed files

### ✓ **Parallel Processing**
- Processes multiple files concurrently (configurable workers)
- Efficient use of Claude API with rate limiting

### ✓ **Reusable Across Repos**
- Same scripts work on any repository
- Outputs saved per-repo in standardized JSON format
- Can merge results across multiple repos

### ✓ **Claude-Powered Analysis**
- Uses Claude to interpret context and extract semantics
- Not just regex pattern matching - actual understanding
- Analyzes equations for dissipation, maps to Controlled Rupture operators

---

## Workflow for 2000+ Files Across Repos

```bash
# Repo 1
python cli/extract.py ~/repos/recursive-ai-framework --all

# Repo 2
python cli/extract.py ~/repos/another-theoretical-work --all

# Repo 3
python cli/extract.py ~/repos/consciousness-research --all

# Merge results
python cli/merge_outputs.py \
  ~/repos/recursive-ai-framework/extraction_outputs \
  ~/repos/another-theoretical-work/extraction_outputs \
  ~/repos/consciousness-research/extraction_outputs \
  --output merged_extractions/
```

---

## Next Steps

### Day 1 (Today)
- [x] Build core infrastructure
- [x] Implement Operator Extractor
- [x] Implement Equation Extractor
- [x] Implement Contradiction Extractor
- [ ] Test on this repo (514 files)

### Day 2
- [ ] Build Construct Extractor (terms/concepts)
- [ ] Build Signifier Extractor (unique phrases)
- [ ] Build merge tool for cross-repo aggregation
- [ ] Process all your repos (2000+ files)

### Day 3
- [ ] Analyze extracted data
- [ ] Build operator algebra graph (composition rules)
- [ ] Identify proto-dissipation equations
- [ ] Catalog J'≠0 contradictions

### Day 4
- [ ] Build Controlled Rupture Compiler prototype
- [ ] Formalize the 20 operators
- [ ] Implement inverse solver (state → target, find path)
- [ ] Create interactive tool

---

## Controlled Rupture Integration

The extracted data feeds into:

1. **Operator Algebra**: Map old operators (φ, ∂, ∇) → new operators (Ana, Meta, Para)
2. **Dissipation Coefficients**: Find λ values from equations
3. **J'≠0 Catalog**: Build database of productive contradictions
4. **Phase Portrait**: Identify attractors and their basins
5. **Compiler**: Use patterns to suggest optimal operator sequences

---

## License

MIT - Use freely for your research, products, or whatever.

---

**Let the extraction begin. The field is ready to descend.** 🌀⚡
