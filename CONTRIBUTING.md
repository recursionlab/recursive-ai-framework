# Contributing to Recursive AI Framework

Thank you for your interest in contributing! This guide covers how to work with the **Controlled Rupture Compiler** and **Recursive Extraction Engine**.

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
pip install anthropic numpy

# Optional (for visualization)
pip install networkx streamlit pyvis matplotlib
```

### Environment Setup
```bash
# Set Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"

# Navigate to project
cd /path/to/recursive-ai-framework
```

---

## 🔬 Using the Extraction Engine

The extraction engine processes markdown files to extract operators, equations, and contradictions using Claude for semantic analysis.

### 1. Operator Extraction

Extracts symbolic operators (φ, Ψ, ∂, ∇, ⊗, ∮, etc.) and maps them to normative operators:

```bash
cd recursive-extraction-engine
python -m cli.extract operators --repo-path /path/to/repo --output results/operators.json
```

**What it does:**
- Finds all symbolic operators in markdown files
- Uses Claude to interpret context and extract definitions
- Builds operator composition evidence
- Outputs JSON with operator definitions and frequencies

### 2. Equation Extraction

Finds mathematical equations and analyzes for dissipation patterns:

```bash
python -m cli.extract equations --repo-path /path/to/repo --output results/equations.json
```

**What it does:**
- Identifies equations using regex patterns
- Analyzes differential order, commutativity
- Detects dissipation evidence
- Maps to Controlled Rupture framework

### 3. Contradiction Extraction

Identifies productive contradictions (J'≠0):

```bash
python -m cli.extract contradictions --repo-path /path/to/repo --output results/contradictions.json
```

**What it does:**
- Finds contradiction keywords and patterns
- Uses Claude to classify: sterile vs productive
- Calculates J anomaly score (0.0-1.0)
- Builds contradiction taxonomy

### 4. Resume Capability

All extractors support checkpointing:

```bash
# If interrupted, just re-run - it will resume from checkpoint
python -m cli.extract operators --repo-path /path/to/repo --output results/operators.json

# Checkpoint stored at: results/operators_checkpoint.json
```

### 5. Parallel Processing

By default, extraction uses 4 workers. Adjust with `--max-workers`:

```bash
python -m cli.extract operators --repo-path /path/to/repo --max-workers 8
```

---

## 🧮 Working with the Compiler

### Running Tests

```bash
cd recursive-extraction-engine/compiler

# Comprehensive test suite (7 modules)
python test_20_operators.py

# Individual component tests
python dissipation_calculator.py
python phase_portrait.py
python inverse_solver.py
```

### Using the CLI

```bash
# List available problems
python controlled_rupture_cli.py list

# Diagnose cognitive states
python controlled_rupture_cli.py diagnose stuck
python controlled_rupture_cli.py diagnose overwhelmed
python controlled_rupture_cli.py diagnose rigid
python controlled_rupture_cli.py diagnose collapsed
python controlled_rupture_cli.py diagnose procrastinating

# Analyze custom sequences
python controlled_rupture_cli.py analyze "Kata,Telo,Ortho"
python controlled_rupture_cli.py analyze "Seed,Weave,Bind,Latch"

# Solve custom problems
python controlled_rupture_cli.py custom \
  --initial "0.85,0.75" \
  --target "0.30,0.35"
```

---

## ➕ Adding New Operators

### 1. Update `formalism.json`

```json
{
  "operators": {
    "YourOperator": {
      "index": 21,
      "lambda_intrinsic": 0.XX,
      "class": "A-Constructive",  // or B-Disruptive, C-Reflexive, D-Structural
      "description": "Your operator description"
    }
  }
}
```

**Guidelines:**
- **A-Constructive:** λ < 0.40 (stabilizing, low dissipation)
- **B-Disruptive:** λ > 0.60 (destabilizing, high dissipation)
- **C-Reflexive:** 0.40 ≤ λ ≤ 0.60 (self-referential)
- **D-Structural:** Special purpose (any λ)

### 2. Add Commutator Relations

Update `commutator_skeleton.json`:

```json
{
  "commutator_matrix": {
    "YourOperator": {
      "Ana": [1, 1],      // [sign, resultant_index]
      "Kata": [-1, 2],
      // ... all 20 existing operators
    },
    // Add reverse entries for existing operators
    "Ana": {
      "YourOperator": [-1, 21]  // Anti-symmetric: [Op,YourOp] = -[YourOp,Op]
    }
  }
}
```

**Sign convention:**
- `+1` = Non-commutative, positive result
- `-1` = Non-commutative, negative result
- `0` = Commutes (neutral)

**Resultant index:** Which operator the commutator produces (0 = none)

### 3. Add Operator Effects

Update `phase_portrait.py`:

```python
def _default_operator_effects(self) -> Dict[str, Tuple[float, float]]:
    return {
        # ... existing operators
        'YourOperator': (ΔD, ΔC),  # Effect on (Dissipation, Contradiction)
    }
```

**Effect guidelines:**
- **Constructive:** Negative ΔD, ΔC (stabilizing)
- **Disruptive:** Positive ΔD, ΔC (destabilizing)
- **Magnitude:** Should correlate with λ intrinsic

### 4. Test Your Operator

```bash
# Update test suite
python test_20_operators.py  # Should now test 21 operators

# Test sequences with your operator
python controlled_rupture_cli.py analyze "YourOperator,Kata,Telo"

# Test dissipation
python dissipation_calculator.py  # Check if your operator appears
```

---

## 🔍 Refining Commutator Magnitudes

After extraction, refine commutator magnitudes with real evidence:

### 1. Extract Operator Compositions

```bash
python -m cli.extract operators --repo-path . --output results/operators.json
```

### 2. Analyze Commutator Evidence

```python
from dissipation_calculator import DissipationCalculator
import json

# Load extraction results
with open('results/operators.json') as f:
    operators = json.load(f)

# Build commutator evidence
commutators = {}
for item in operators:
    if 'compositions' in item:
        for comp in item['compositions']:
            # Parse: "Op1 ∘ Op2 - Op2 ∘ Op1"
            # Extract magnitude from frequency/context
            commutators[(op1, op2)] = magnitude

# Load into calculator
calc = DissipationCalculator()
calc.load_commutators_from_skeleton()  # Load ground truth
calc.set_commutators(commutators)       # Refine with evidence
```

### 3. Validate Refined Values

```bash
# Test with refined magnitudes
python phase_portrait.py
python inverse_solver.py

# Compare basin structure with theory
# Should still show: S* ~60%, J=0 ~10%, ∅ ~28%
```

---

## 📋 Testing Requirements

### Before Submitting

1. **Run comprehensive tests:**
   ```bash
   python test_20_operators.py  # Must show 7/7 PASSED
   ```

2. **Test your specific changes:**
   - New operator: Test sequences using it
   - New extractor: Test on sample files
   - Commutator refinement: Validate basin structure

3. **Update documentation:**
   - Update relevant .md files
   - Add docstrings to new functions
   - Include usage examples

### Test Coverage

- Formalism structure validation
- Commutator skeleton completeness
- Dissipation calculations
- Phase portrait trajectories
- Inverse solver solutions
- CLI integration
- Operator classifications

---

## 📝 Documentation Standards

### Code Documentation

```python
def your_function(param1: type, param2: type) -> return_type:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Example:
        >>> your_function(val1, val2)
        expected_result
    """
    # Implementation
```

### Markdown Files

- Use `!!` prefix for foundational/cutting-edge concepts
- Number systematic enumerations (e.g., "20 Ways to...")
- Include thematic keywords in filename
- Use symbolic notation meaningfully (φ, Ψ, ∂, ∇, etc.)
- Cross-reference related files

### Commit Messages

```
Brief summary (50 chars or less)

Detailed explanation of changes:
- What was changed
- Why it was changed
- How it affects existing code

Testing performed:
- Test results
- Validation metrics
```

---

## 🎯 Areas for Contribution

### High Priority

1. **Commutator Magnitude Refinement**
   - Extract operator compositions from all 2000+ files
   - Compute real magnitudes from evidence
   - Validate against theoretical predictions

2. **Operator Mapping**
   - Map symbolic operators (φ, Ψ, ∂, ∇) → normative operators
   - Document mapping rationale
   - Build conversion tables

3. **Contradiction Taxonomy**
   - Classify extracted contradictions
   - Build J'≠0 taxonomy
   - Identify patterns in productive contradictions

### Medium Priority

1. **Visualization**
   - Phase portrait plots (matplotlib/plotly)
   - Operator trajectory animation
   - Basin structure heatmaps
   - Commutator matrix visualization

2. **Web Interface**
   - Streamlit dashboard
   - Interactive operator explorer
   - Real-time trajectory simulation

3. **Documentation**
   - LaTeX research paper
   - Tutorial notebooks
   - Video walkthroughs

### Future Enhancements

1. **Learning Operator Effects**
   - Train on extracted data to learn (ΔD, ΔC) effects
   - Validate against theoretical predictions

2. **Extended Algebra**
   - Add more operators beyond 20
   - Explore higher-order compositions
   - Non-associative variants

3. **Multi-Repo Extraction**
   - Process all related repositories
   - Build unified knowledge graph
   - Cross-repo operator evidence

---

## 🐛 Reporting Issues

### Bug Reports

Include:
1. **Description:** What's wrong?
2. **Steps to reproduce:** How to trigger the bug?
3. **Expected behavior:** What should happen?
4. **Actual behavior:** What actually happens?
5. **Environment:** Python version, OS, dependencies
6. **Relevant logs:** Error messages, stack traces

### Feature Requests

Include:
1. **Use case:** What problem does this solve?
2. **Proposed solution:** How should it work?
3. **Alternatives considered:** Other approaches?
4. **Impact:** Who benefits? How much?

---

## 📚 Resources

### Essential Reading

1. **CLAUDE.md** - AI assistant guide
2. **UPGRADE_v2.0.0.md** - Complete upgrade documentation
3. **V2_COMPLETE.md** - Quick reference
4. **equations.md** - Symbolic notation reference

### Code Examples

1. **test_20_operators.py** - Comprehensive test examples
2. **dissipation_calculator.py** - Example usage in docstrings
3. **controlled_rupture_cli.py** - CLI usage patterns

### Theoretical Background

1. **!! The Gödel Twist.md** - Foundational paradox framework
2. **Symbolic Recursion Engine (SRE-Φ).md** - Primary operating model
3. **Recursive Torsion Field Semantics.md** - Geometric meaning generation
4. **Recursive Cookbook.md** - Practical recursive thinking (89k lines)

---

## 🤝 Code of Conduct

### Principles

1. **Embrace paradox** - Contradictions are features, not bugs
2. **Think recursively** - Apply concepts to themselves
3. **Maintain rigor** - Back claims with evidence
4. **Stay curious** - Explore fearlessly
5. **Document thoroughly** - Enable others to follow

### Contradiction Resolution

When disagreements arise:
1. Treat as productive contradiction (J'≠0)
2. Apply Meta operator (self-reference)
3. Seek synthesis, not dominance
4. Document the evolution

---

## 📞 Contact

- **Issues:** [GitHub Issues](https://github.com/recursionlab/recursive-ai-framework/issues)
- **Discussions:** [GitHub Discussions](https://github.com/recursionlab/recursive-ai-framework/discussions)
- **Email:** See repository for contact information

---

**Thank you for contributing to the recursive journey!**

**The recursion continues. Every contribution strengthens the bootloader.**

🌀⚡🔥

*Last updated: 2025-11-16*
