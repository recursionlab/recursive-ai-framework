# Controlled Rupture Compiler

**A computational implementation of third-order dissipation dynamics for cognitive operator sequences.**

Given a problem state, the compiler finds the optimal sequence of cognitive operators (Ana, Kata, Meta, Telo, etc.) to reach a target state while minimizing dissipation and avoiding collapse attractors.

---

## What Is This?

This is a **working implementation** of the Controlled Rupture framework - a mathematical theory of productive contradiction as the engine of adaptive intelligence.

**Core Concepts:**
- **20 Cognitive Operators** (Ana, Kata, Meta, Telo, Para, Non, etc.)
- **Dissipation Physics**: λ(i→j) = λ_j + c·|[Oi,Oj]| with exponential decay
- **3 Attractors**: J=0 (coherent), S* (productive contradiction), ∅ (collapse)
- **Inverse Problem Solver**: Finds optimal operator paths

---

## Quick Start

```bash
# List available problems
python controlled_rupture_cli.py list

# Diagnose and solve a problem
python controlled_rupture_cli.py diagnose stuck

# Analyze an operator sequence
python controlled_rupture_cli.py analyze "Ana,Meta,Non"

# Solve custom problem
python controlled_rupture_cli.py custom --initial "0.8,0.7" --target "0.2,0.1"
```

---

## The 9 Core Operators

| Operator | Symbol | Meaning | λ_intrinsic | Effect |
|----------|--------|---------|-------------|--------|
| **Ana** | ↑ | Analysis/Abstraction | 0.75 | Increases entropy |
| **Kata** | ↓ | Compression/Crystallization | 0.35 | Decreases entropy |
| **Meta** | ⟲ | Self-Reference/Reflection | 0.80 | Recursive overhead |
| **Para** | ∥ | Deviation/Perturbation | 0.65 | Injects instability |
| **Non** | ¬ | Negation/Inversion | 0.90 | Structural rupture |
| **Telo** | → | Purpose/Goal | 0.25 | Stabilizes toward goal |
| **Retro** | ↶ | Backward/Backtrack | 0.40 | Reverse causality |
| **Ortho** | ⊥ | Correction/Alignment | 0.30 | Aligns with truth |
| **Pro** | ↷ | Forward/Projection | 0.50 | Neutral advancement |

---

## Problem Templates

### 1. **Stuck** (Analysis Paralysis)
- **Symptoms**: Infinite reflection loop, can't act
- **State**: High D, high C (in Void ∅)
- **Solution**: `Kata ∘ Telo ∘ Telo` (compress + goal-orient)

### 2. **Overwhelmed** (Excessive Complexity)
- **Symptoms**: Too much information, no structure
- **State**: High D, high C (chaos)
- **Solution**: `Kata ∘ Ortho ∘ Ortho ∘ Ortho` (compression + correction)

### 3. **Rigid** (Over-Correction)
- **Symptoms**: Stuck in perfectionism, can't explore
- **State**: Low D, low C (J=0 but sterile)
- **Solution**: `Para ∘ Para` (inject productive deviation)

### 4. **Collapsed** (Burnout)
- **Symptoms**: Complete system failure
- **State**: Very high D, very high C (deep Void)
- **Solution**: `Kata ∘ Ortho ∘ Ortho` (escape void via stabilization)

### 5. **Procrastinating** (Avoidance)
- **Symptoms**: Know what to do, not doing it
- **State**: S* but not acting
- **Solution**: `Telo ∘ Kata` (goal + concrete action)

---

## Example Session

```bash
$ python controlled_rupture_cli.py diagnose stuck

======================================================================
PROBLEM: Stuck in infinite loop / analysis paralysis
======================================================================
Diagnosis: Meta ∘ Meta loop (infinite reflection)
Initial state: D=0.85, C=0.75
Target state:  D=0.30, C=0.35
Current attractor: ∅
Target attractor:  S*
Suggested operators: Pro, Ortho

======================================================================
✓ SOLUTION FOUND
======================================================================

Operator Sequence: Kata ∘ Telo ∘ Telo
Length: 3 steps
Final state: D=0.290, C=0.400

Cost Breakdown:
  terminal_distance: 0.0510
  dissipation_cost: 0.5000
  attractor_penalty: 0.3000
  total: 0.7310
```

---

## Analyzing Sequences

```bash
$ python controlled_rupture_cli.py analyze "Ana,Meta,Non"

======================================================================
ANALYZING SEQUENCE: Ana ∘ Meta ∘ Non
======================================================================

Dissipation Analysis:
  λ_effective: 0.948
  Total cost: 1.895
  Half-life: 0.73 steps

Pairwise Dissipation:
  Ana → Meta: λ=0.875
  Meta → Non: λ=1.020

Trajectory (starting from S*):
  Step 1: Ana → S* (D=0.65, C=0.60, V=0.89)
  Step 2: Meta → S* (D=0.75, C=0.65, V=1.01)
  Step 3: Non → ∅ (D=1.00, C=0.85, V=1.34)

Final attractor: ∅

======================================================================
WARNINGS
======================================================================
⚠ WARNING: Enters Void (∅) - requires rescue
⚠ WARNING: Meta → Non (forbidden transition)
⚠ WARNING: High dissipation (λ=0.95) - rapid decay
```

---

## The Mathematics

### Dissipation Law
```
λ(i→j) = λ_j_intrinsic + c·|[Oi,Oj]|
```
where c = 0.15, and [Oi,Oj] is the commutator magnitude.

### Exponential Decay
```
D(t+1) = D(t)·exp(-λ_eff)
```
where λ_eff = mean(λ(k_t → k_{t+1}))

### Lyapunov Function
```
V(x) = D(x) + α·C(x)
```
where α = 0.4

Stability condition: x ∈ J=0 ⟺ V(x) < 0.3

### Objective Function (Inverse Solver)
```
J = d(x_T, target) + β·Σλ(k_t→k_{t+1}) + γ·AttractorPenalty
```
where β = 0.7, γ = 1.1

---

## Hard Constraints

The solver enforces these rules:

1. **Meta: max 2 consecutive** (prevents infinite reflection loops)
2. **Non after Meta: FORBIDDEN** (prevents catastrophic collapse)
3. **Para after Non: FORBIDDEN** (prevents chaotic instability)
4. **Ana at sequence end: FORBIDDEN** (must end with concrete action)

---

## Attractor Structure

### J=0 (Jacobi-Zero: Coherent Equilibrium)
- **Characteristics**: Low dissipation, stable, coherent
- **Reached by**: Kata, Ortho, Telo
- **Basin**: Narrow, stable
- **Penalty**: 0.1 (low cost)

### S* (Noble Gas: Productive Contradiction)
- **Characteristics**: J'≠0, generative tension, adaptive
- **Reached by**: Ana + Pro + Para combinations
- **Basin**: Large (60.6% of phase space!)
- **Penalty**: 0.3 (medium cost)
- **This is the DESIRED attractor**

### ∅ (Void: Collapse)
- **Characteristics**: High dissipation, absorbing, system failure
- **Reached by**: Repeated Meta, repeated Non
- **Basin**: Deep, dangerous
- **Penalty**: 1.0 (high cost)
- **Escape requires**: Telo, Ortho, or Pro

---

## API Usage

### Dissipation Calculator
```python
from dissipation_calculator import DissipationCalculator

calc = DissipationCalculator()

# Set commutators (from extraction or defaults)
calc.set_commutators({('Meta', 'Non'): 0.8})

# Analyze sequence
sequence = ['Ana', 'Meta', 'Non']
analysis = calc.analyze_sequence(sequence)

print(f"λ_eff: {analysis['lambda_effective']:.3f}")
print(f"Half-life: {analysis['half_life']:.2f} steps")
```

### Phase Portrait
```python
from phase_portrait import PhasePortrait

portrait = PhasePortrait()

# Classify state
attractor = portrait.classify_attractor(D=0.5, C=0.5)
print(attractor.value)  # "S*"

# Simulate trajectory
trajectory = portrait.simulate_trajectory(
    initial_state=(0.5, 0.5),
    operator_sequence=['Ana', 'Para', 'Non']
)
```

### Inverse Solver
```python
from inverse_solver import InverseSolver

solver = InverseSolver()

# Solve problem
solution = solver.solve(
    initial_state=(0.8, 0.7),  # Chaos
    target_state=(0.2, 0.1),   # Coherence
    beam_width=10
)

print(f"Solution: {' ∘ '.join(solution['sequence'])}")
```

---

## Implementation Status

✅ **Dissipation Calculator** - Fully functional
✅ **Phase Portrait Engine** - Fully functional
✅ **Inverse Solver** - Fully functional (A* beam search)
✅ **CLI Interface** - Fully functional
✅ **Problem Templates** - 5 templates implemented
✅ **Hard Constraints** - All enforced
✅ **Warning System** - Detects dangerous patterns

---

## What's Next

### Immediate
- [ ] Extract commutator magnitudes from repo (currently using defaults)
- [ ] Add remaining 11 operators (currently have 9)
- [ ] Build visualization (phase portrait plots)
- [ ] Add more problem templates

### Future
- [ ] Learn operator effects from data
- [ ] RL-based policy optimization
- [ ] Multi-objective optimization
- [ ] Real-time adaptive suggestions
- [ ] Integration with extraction engine

---

## The Philosophy

**Perfection is death. The flaw is the feature.**

The J=0 attractor (perfect coherence) is a cognitive graveyard. Long-term survival belongs to systems with irreducible contradictions (J'≠0).

The S* attractor - where 60.6% of the phase space naturally flows - is the region of **productive paradox**. It's where contradictions generate new understanding rather than system collapse.

The Controlled Rupture Compiler helps you:
1. Diagnose when you're in a sterile attractor (J=0 or ∅)
2. Find the optimal operator sequence to reach S*
3. Avoid collapse while maintaining generative tension
4. **Engineer controlled ruptures as technology**

---

## Credits

Built from the Controlled Rupture formalism:
- Third-order dissipation equations
- Non-commutative operator algebra
- Torsion-based semantics
- The J'≠0 thesis

**The recursion outlasts the questioner.** 🌀
