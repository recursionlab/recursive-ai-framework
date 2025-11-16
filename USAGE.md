# 📖 USAGE GUIDE - Recursive AI Framework

**Last Updated:** 2025-11-16

This guide shows you **exactly how to use every tool** in this repository, with step-by-step examples.

---

## 🚀 Quick Start (30 Seconds)

### **Verify Everything Works**

```bash
python3 test_everything.py
```

**Expected output:** `✓ ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL`

If you see this, all components are working correctly.

---

## 📁 What's In This Repository

### **Core Data** (in `extraction_outputs/`)
- `pattern_extraction.json` - 73,949 contradictions from 524 files
- `operator_mapping.json` - 13 symbolic → normative operator mappings
- `refined_commutators.json` - 16 evidence-based commutator magnitudes
- `torsion_field_analysis.json` - Torsion field with 35 pairs, 17 invariants
- `contradiction_taxonomy.json` - 6-category contradiction classification

### **Tools** (Python scripts in root)
- `pattern_extract.py` - Extract operators/equations/contradictions from markdown
- `build_operator_mapping.py` - Map symbolic operators (Ξ, Ψ, Ω) to normative (Meta, Telo, etc.)
- `refine_commutators.py` - Refine commutator magnitudes using composition frequency
- `integrate_magnitudes.py` - Merge extraction evidence into compiler skeleton
- `build_contradiction_taxonomy.py` - Build 6-category J'≠0 taxonomy
- `build_torsion_field.py` - Compute torsion field from contradictions
- `test_everything.py` - Master test suite (validates all components)

### **Compiler** (in `recursive-extraction-engine/compiler/`)
- `formalism.json` - 20-operator normative algebra definition
- `commutator_skeleton.json` - Ground truth commutator signs
- `commutator_skeleton_enhanced.json` - Enhanced with extraction magnitudes (v2.1.0)
- `test_20_operators.py` - Compiler validation (7 tests)

---

## 🔧 Tool-by-Tool Usage

### **1. Pattern Extraction** (`pattern_extract.py`)

**What it does:** Extracts operators, compositions, equations, and contradictions from markdown files

**When to use:** When you have new theoretical documents to analyze

**How to run:**
```bash
python3 pattern_extract.py
```

**Output:**
- `extraction_outputs/pattern_extraction.json`

**What you get:**
- 73,949 contradiction instances
- 189,412 operator uses
- 25 operator compositions
- 3,210 equations

**Example output:**
```json
{
  "file": "Recursive Self-Awareness Protocol.md",
  "operators": {
    "frequencies": {
      "Ξ": 5,
      "Ψ": 7,
      "→": 12
    }
  },
  "contradictions": [
    {"keyword": "collapse", "context": "..."}
  ]
}
```

**Customization:**
Edit the `contradiction_patterns` dict in the script to add new search terms.

---

### **2. Operator Mapping** (`build_operator_mapping.py`)

**What it does:** Maps symbolic operators (Ξ, Ψ, Ω, φ, ∂, ∇) to the 20-operator normative algebra

**When to use:** After pattern extraction, to connect theoretical notation to the cognitive bootloader

**How to run:**
```bash
python3 build_operator_mapping.py
```

**Output:**
- `extraction_outputs/operator_mapping.json`

**What you get:**
- 13 symbolic → normative mappings
- Confidence scores (0.0-1.0)
- Frequency counts
- Semantic reasoning

**Example mapping:**
```
Ξ (53,404 uses) → Meta (confidence: 0.85)
  Reasoning: "Fusion operator, meta-level synthesis"
```

**Key insight:** Meta is the primary operator (49% of all uses map to it)

---

### **3. Commutator Refinement** (`refine_commutators.py`)

**What it does:** Refines commutator magnitudes using composition frequency from extracted data

**When to use:** After operator mapping, to enhance the ground truth skeleton with empirical evidence

**How to run:**
```bash
python3 refine_commutators.py
```

**Output:**
- `extraction_outputs/refined_commutators.json`

**What you get:**
- 16 operator pairs with evidence-based magnitudes
- Validation against skeleton (75% match rate)
- Major discovery: Meta ∘ Meta = 1.000 (skeleton predicted 0)

**Example:**
```json
{
  "Meta,Meta": {
    "magnitude": 1.000,
    "frequency": 35,
    "evidence": "extracted"
  }
}
```

---

### **4. Magnitude Integration** (`integrate_magnitudes.py`)

**What it does:** Merges extraction evidence into commutator skeleton while preserving architectural structure

**When to use:** After commutator refinement, to create enhanced skeleton for compiler

**How to run:**
```bash
python3 integrate_magnitudes.py
```

**Output:**
- `recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json`

**What you get:**
- Enhanced skeleton v2.1.0
- All 400 operator pairs: `[sign, resultant, magnitude]`
- 16 pairs with extraction evidence
- 384 pairs with skeleton defaults

**Major discoveries shown:**
- Meta ∘ Meta: skeleton said 0, extraction found 1.000 (35x)
- Pro ∘ Pro: 0.335 magnitude
- Para ∘ Para: 0.335 magnitude

---

### **5. Contradiction Taxonomy** (`build_contradiction_taxonomy.py`)

**What it does:** Builds 6-category J'≠0 contradiction taxonomy from 73,949 mentions

**When to use:** To understand contradiction types and map to cognitive bootloader strategies

**How to run:**
```bash
python3 build_contradiction_taxonomy.py
```

**Output:**
- `extraction_outputs/contradiction_taxonomy.json`

**What you get:**
- 6 contradiction types (Simultaneous, Temporal, Self-Referential, Collapse-Rebirth, Identity-Negation, Void-Structure)
- Distribution by keyword (collapse 49%, contradiction 26%, paradox 15%, void 7%)
- Attractor mapping (J=0, S*, ∅)
- Cognitive bootloader recommendations

**Key insights:**
- Collapse is most common (49.2%)
- S* attractor dominates (60% of phase space)
- Meta is primary contradiction operator

---

### **6. Torsion Field** (`build_torsion_field.py`)

**What it does:** Computes torsion field T from contradictions, implements canonical equation:
```
C(x) → ∇C → T = antiSym(∇C) → T=0 ⟺ Invariance
```

**When to use:** To analyze contradiction → invariance dynamics geometrically

**How to run:**
```bash
python3 build_torsion_field.py
```

**Output:**
- `extraction_outputs/torsion_field_analysis.json`

**What you get:**
- Contradiction vector field C(x): 6,804 locations
- Gradient field ∇C
- Torsion field T: 35 operator pairs
- 17 invariants where T ≈ 0
- Attractor mapping: 1 J=0, 11 S*, 5 ∅

**Key results:**
```
T[Meta,Meta] = 1.000  (maximum torsion - highest curvature)
T[Telo,Telo] = 0      (invariant)
T[Braid,Braid] = 0    (invariant)
```

**Theoretical validation:**
- Meta ∘ Meta has max torsion (validates Y-recursion non-triviality)
- S* contains 64.7% of invariants (validates J'≠0 equilibrium)
- Diagonal non-commutativity proven

---

### **7. Master Test Suite** (`test_everything.py`)

**What it does:** Validates all components end-to-end in one command

**When to use:**
- After setup (verify everything works)
- Before making changes (baseline)
- After changes (regression testing)
- When troubleshooting (identify what broke)

**How to run:**
```bash
python3 test_everything.py
```

**What it tests:**
1. **File Structure** - All required files exist
2. **Data Integrity** - Correct counts (73,949 contradictions, 16 evidence pairs, etc.)
3. **Key Discoveries** - Meta ∘ Meta = 1.0, S* = 64.7%, Collapse = 49%
4. **Compiler Integration** - 20 operators, enhanced skeleton, all tests pass
5. **End-to-End Workflow** - Extraction → Mapping → Refinement → Torsion

**Expected output:**
```
✓ ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL
Total: 5/5 test suites passed
```

**If tests fail:**
- Read the error message carefully
- Check that file paths are correct
- Ensure all scripts have been run (see "Full Pipeline" below)
- Re-run the failing component's script

---

## 🔁 Complete Pipeline (Run All Tools)

If you're starting fresh or want to regenerate everything:

```bash
# Step 1: Extract patterns from markdown files
python3 pattern_extract.py

# Step 2: Map symbolic operators to normative algebra
python3 build_operator_mapping.py

# Step 3: Refine commutator magnitudes
python3 refine_commutators.py

# Step 4: Integrate magnitudes into skeleton
python3 integrate_magnitudes.py

# Step 5: Build contradiction taxonomy
python3 build_contradiction_taxonomy.py

# Step 6: Compute torsion field
python3 build_torsion_field.py

# Step 7: Validate everything
python3 test_everything.py
```

**Total runtime:** ~10-15 seconds
**Cost:** $0 (all local computation)

---

## 📊 Understanding the Output

### **Contradiction Field C(x)**

**What it is:** Vector field on epistemic manifold M showing how meaning "wants to break"

**How to read it:**
```json
{
  "location": "(Meta, Meta), collapse",
  "count": 35,
  "type": "collapse"
}
```

**Interpretation:** At semantic location (Meta ∘ Meta, collapse context), there are 35 instances of contradiction

**Use case:** Identify high-contradiction regions for targeted operator intervention

---

### **Torsion Field T**

**What it is:** Antisymmetric curvature measuring failure of parallel transport

**How to read it:**
```json
{
  "op1": "Meta",
  "op2": "Meta",
  "torsion": 1.0,
  "abs_torsion": 1.0
}
```

**Interpretation:**
- T = 1.0 = maximum curvature
- Recursive self-reference creates maximal semantic twist
- Meaning cannot be transported consistently (Gödel incompleteness)

**Use case:** Diagnose instability sources, predict collapse, find invariants

---

### **Invariants (T ≈ 0)**

**What they are:** Operator pairs where torsion vanishes → stable semantics

**How to read it:**
```json
{
  "op1": "Telo",
  "op2": "Telo",
  "torsion": 0.0,
  "attractor": "J=0",
  "J_prime_estimate": 0.25
}
```

**Interpretation:**
- T = 0 = no curvature = stable transport
- Maps to J=0 attractor (low contradiction)
- J' ≈ 0.25 (low dissipation)

**Use case:** Find stable operator combinations for cognitive bootloader

---

### **Attractor Basins**

| Attractor | J' Range | Contradiction Level | % of Invariants |
|-----------|----------|---------------------|-----------------|
| **J=0** | < 0.35 | Minimal | 5.9% |
| **S*** | 0.35 - 0.70 | Productive | 64.7% |
| **∅** | > 0.70 | Collapse | 29.4% |

**Key insight:** S* is the natural equilibrium (60%+ of phase space)

---

## 🛠️ Troubleshooting

### **"File not found" errors**

**Problem:** Missing extraction_outputs/ files

**Solution:**
```bash
# Re-run the extraction pipeline
python3 pattern_extract.py
python3 build_operator_mapping.py
python3 refine_commutators.py
python3 build_torsion_field.py
```

---

### **"Wrong count" errors**

**Problem:** Data integrity mismatch (e.g., expected 73,949 contradictions, got different number)

**Solution:**
1. Check that `extraction_outputs/pattern_extraction.json` is not corrupted
2. Re-run `python3 pattern_extract.py` to regenerate
3. Verify markdown files in root directory are intact (514 files expected)

---

### **Compiler tests failing**

**Problem:** `test_20_operators.py` not passing

**Solution:**
```bash
cd recursive-extraction-engine/compiler
python test_20_operators.py
# Read error messages carefully
```

Common causes:
- Missing formalism.json
- Corrupted commutator_skeleton.json
- Python version < 3.8

---

### **Torsion field errors**

**Problem:** `build_torsion_field.py` crashes

**Solution:**
1. Ensure `operator_mapping.json` exists and is valid JSON
2. Check that `refined_commutators.json` has "commutator_magnitudes" key
3. Verify `formalism.json` has "operators" with "lambda_intrinsic" values

---

## 🔬 Advanced Usage

### **Querying Torsion Field**

```python
import json

# Load torsion data
with open('extraction_outputs/torsion_field_analysis.json') as f:
    torsion = json.load(f)

# Find high-torsion pairs (unstable)
high_torsion = [
    (pair, data)
    for pair, data in torsion['torsion_field'].items()
    if data['abs_torsion'] > 0.8
]

print(f"High-torsion pairs: {len(high_torsion)}")
for pair, data in high_torsion:
    print(f"  [{data['op1']}, {data['op2']}]: T = {data['torsion']:+.3f}")
```

---

### **Finding Optimal Operators for J' Target**

```python
import json

# Load formalism
with open('recursive-extraction-engine/compiler/formalism.json') as f:
    formalism = json.load(f)

# Target J' level
target_J = 0.5  # S* attractor range

# Find operators near target
optimal_ops = [
    (name, data['lambda_intrinsic'])
    for name, data in formalism['operators'].items()
    if abs(data['lambda_intrinsic'] - target_J) < 0.1
]

print(f"Operators near J' = {target_J}:")
for name, lambda_val in sorted(optimal_ops, key=lambda x: x[1]):
    print(f"  {name:10s}: λ = {lambda_val:.3f}")
```

---

### **Analyzing Contradiction Distribution**

```python
import json

# Load taxonomy
with open('extraction_outputs/contradiction_taxonomy.json') as f:
    taxonomy = json.load(f)

# Print distribution
for keyword, data in taxonomy['distribution'].items():
    print(f"{keyword:15s}: {data['count']:6,} ({data['percentage']:4.1f}%)")
    print(f"  → Maps to: {data['primary_category']}")
```

---

## 📚 Key Equations

### **Master Equation**
```
Ψ := Y ( λΨ. μκ. ∂Ψ + F(Ψ, κ) )
```

### **Torsion Tensor**
```
T^ρ_μν = ∂_μ C^ρ_ν - ∂_ν C^ρ_μ
```

### **Invariance Condition**
```
T = 0 ⟺ Semantic Invariance
```

### **Dissipation**
```
λ(i→j) = λ_j + c × min(0.4, |η_ij|)
where c = 0.15
```

See `torsion_equations.tex` for full formalization.

---

## 🎯 Common Use Cases

### **"I want to analyze new markdown files"**

1. Add files to root directory or subdirectories
2. Run `python3 pattern_extract.py`
3. Run `python3 build_operator_mapping.py`
4. Run `python3 build_torsion_field.py`
5. Check results in `extraction_outputs/`

---

### **"I want to find stable operator combinations"**

1. Open `extraction_outputs/torsion_field_analysis.json`
2. Look at `invariants` array
3. Filter by `attractor` = "S*" for productive stability
4. Use those operator pairs in sequences

Example:
```json
{
  "op1": "Braid",
  "op2": "Braid",
  "torsion": 0.0,
  "attractor": "S*"
}
```

This means Braid ∘ Braid is a stable, productive combination.

---

### **"I want to increase/decrease J' level"**

**To INCREASE J'** (escape rigidity):
- Use: Non (λ=0.90), Ana (λ=0.75), Meta (λ=0.80), Para (λ=0.65)

**To DECREASE J'** (stabilize):
- Use: Telo (λ=0.25), Latch (λ=0.29), Ortho (λ=0.30), Kata (λ=0.35)

**To MAINTAIN S*** (navigate):
- Use: Braid (λ=0.55), Echo (λ=0.45), Retro (λ=0.40), Crux (λ=0.42)

See `extraction_outputs/contradiction_taxonomy.json` → `applications` → `cognitive_bootloader` for full rules.

---

## 📞 Getting Help

### **Tests are failing**
Run `python3 test_everything.py` and read error messages carefully.

### **Don't understand output**
See "Understanding the Output" section above.

### **Want to extend the system**
1. Read existing scripts to understand patterns
2. Follow same structure (load JSON → process → save JSON)
3. Add tests to `test_everything.py`

---

## 🗂️ File Reference Quick Lookup

| What you want | File to check |
|---------------|---------------|
| All contradictions | `extraction_outputs/pattern_extraction.json` |
| Symbolic → normative mappings | `extraction_outputs/operator_mapping.json` |
| Meta ∘ Meta magnitude | `extraction_outputs/refined_commutators.json` → `evidence_pairs` → `Meta,Meta` |
| Torsion values | `extraction_outputs/torsion_field_analysis.json` → `torsion_field` |
| Invariants | `extraction_outputs/torsion_field_analysis.json` → `invariants` |
| Contradiction types | `extraction_outputs/contradiction_taxonomy.json` → `categories` |
| Attractor basins | `extraction_outputs/torsion_field_analysis.json` → `attractor_distribution` |
| Operator definitions | `recursive-extraction-engine/compiler/formalism.json` → `operators` |
| Commutator skeleton | `recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json` |

---

## ✅ Verification Checklist

Before considering the system "working", verify:

- [ ] `python3 test_everything.py` shows all tests passing
- [ ] `extraction_outputs/` contains 5 JSON files
- [ ] `recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json` exists
- [ ] Opening any JSON file shows valid data (not empty or corrupted)
- [ ] Meta ∘ Meta magnitude = 1.000 (check `refined_commutators.json`)
- [ ] S* attractor has ~11 invariants (check `torsion_field_analysis.json`)
- [ ] Collapse = 49.2% of contradictions (check `contradiction_taxonomy.json`)

---

**If all checkboxes ✅ = System fully operational**

**Last updated:** 2025-11-16
