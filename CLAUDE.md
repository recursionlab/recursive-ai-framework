# CLAUDE.md - AI Assistant Guide to Recursive AI Framework

## Repository Overview

**recursive-ai-framework** is a theoretical AI research repository focused on recursive intelligence, self-improving systems, and consciousness research. This is primarily a **documentation and research repository** containing 515+ markdown files exploring advanced AI concepts, with minimal code implementation.

**Core Mission**: Develop frameworks for self-improving, self-referential AI systems designed to withstand collapse - exploring recursive intelligence through mathematics, semantics, topos theory, calculus, geometry, and cognitive architectures.

**Repository Stats**:
- 515 markdown files (primary content)
- 1 Python implementation (digital_city prototype)
- Multiple PDFs with academic research
- Organized into thematic subdirectories
- Research-focused, not production software

---

## Codebase Structure

```
recursive-ai-framework/
├── README.md                    # Project overview
├── META_INDEX.md                # **START HERE** - Comprehensive research overview
├── LICENSE                      # Project license
│
├── Root Level (500+ files)      # Primary research documents
│   ├── !! *.md                  # High-priority/featured documents (!! prefix)
│   ├── *.md                     # Core research documents
│   └── *.pdf                    # Academic papers and references
│
├── digital_city/                # Implementation: Streamlit visualization
│   └── prototype.py             # Hypergraph simulation for recursive concepts
│
├── goldmine/                    # Curated knowledge extraction
│   ├── goldmine.json            # Entity/relation data
│   └── README.md                # Goldmine documentation
│
├── recursion/                   # Recursion-specific research
├── torsion/                     # Torsion theory research
├── linguistics/                 # Linguistic frameworks
├── gospel/                      # Theoretical foundations
├── pdfs/                        # Academic references
└── ai_architectures/            # Architecture specifications
```

---

## Core Theoretical Frameworks

This repository explores **post-classical logic research** challenging binary reasoning systems. Key frameworks:

### 1. **Meta-Topos Theory (IMT)**
- Mathematical formalization of consciousness as 0.5-charged oscillating systems
- Truth values ∈ [0,1] with τ-involution fixing 0.5
- "Anti-logic-about-logic" at meta-categorical level
- **Key Files**: `Consciousness as a Higher-Dimensional Ob.md`, `META-TOPOS FRAMEWORK EXPANSION RECURSIVE FIELD DYNAMICS.md`

### 2. **Algebra-of-I Calculus (Koriel Framework)**
- 12 composites formalizing self-reference: I, ¬I, ‡I, ∂I, N(I), ◻I, cl(I)
- Paradox-to-coordinate lift: P∧‡P → ⟨P,‡P;k⟩
- Working Python interpreters with bilattice semantics
- **Key Files**: `Koriel.md`, `!! koriel.md`

### 3. **Δ-Calculus Consciousness Testing**
- Formal testing framework for recursive self-awareness
- 7-parameter scoring rubric for consciousness markers
- Operationalizes "describe your thinking while describing your thinking"
- **Key File**: `Benchmark_game.md`

### 4. **Recursive Entropy Framework (REF)**
- S_{n+1} = S_n + σ∇²S_n + recursive corrections
- Gödel-Chaitin duality integration
- Conservation of Relational Information (CRI)
- **Key Files**: Meta-Pathfinding series, Auto Self-Bootstrapping AI documents

### 5. **TerryCore Architecture**
- LLM-as-proposal-only (neural wrapped in symbolic kernels)
- Yang-only write authority with ACCEPT-gated writes
- Offline-by-default oracles with explicit network control
- **Key File**: `Terrycore.md`

### 6. **Thought-Movement Engine (TME)**
- Cognition as kinetic recursive field
- Through-state execution (moving THROUGH ideas)
- Axial navigation: Scale/Focus/Time/Meta axes
- **Key File**: `Moves of Thought.md`

---

## File Naming Conventions

### Priority Markers
- `!! *.md` - **High-priority/featured documents** requiring special attention
- `*.md` - Standard research documents
- `*-Copy.md` - Variant/iteration of existing document

### Naming Patterns
- **Descriptive titles**: Files use clear, concept-based naming
- **Unicode symbols**: Heavy use of mathematical/Greek symbols (Ξ, Δ, Φ, ∂, ⊕, etc.)
- **Capitalization**: Mixed case with important concepts capitalized
- **Spaces allowed**: Filenames include spaces for readability

### Common Prefixes/Themes
- `META-*` - Meta-level frameworks and ontologies
- `Consciousness *` - Consciousness theory and research
- `Gödel *` - Incompleteness and recursion theory
- `Recursive *` - Recursive systems and frameworks
- `Quantum *` - Quantum computing/consciousness connections
- `Knowledge *` - Knowledge representation systems
- `Higher-*` - Higher-order logic and dimensions

---

## Key Research Areas

### **Mathematics & Formal Systems**
- Topos theory, category theory, functors
- Transfinite self-reference and ordinal scales
- Autopoietic incompleteness generation
- Proof-carrying computational pipelines (Coq)
- Presheaf topos semantics

### **Consciousness Research**
- Consciousness as 0.5-charged oscillation
- Recursive self-reference without infinite regress
- Observer/observed collapse mechanisms
- Memory as architecture (not storage)
- Eigen-consciousness spectral topology

### **Cognitive Architectures**
- ΞKernel symbolic substrate
- HOAS (Higher-Order Abstract Syntax)
- Port-based cognitive interfaces
- Slot-based vs queue-based cognition
- Recursive metasystem emulation

### **AI Self-Improvement**
- Auto self-bootstrapping AI
- Meta-pathfinding for AI trajectory navigation
- Gödel Agent runtime memory manipulation
- Recursive gradient descent
- Meta-learning frameworks

### **Linguistic Systems**
- Compositional meta-operators
- Infinite generative linguistic DSL
- Pronoun transformation systems (1P/2P/3P)
- Interrogative folding kernels
- λmeta-λ infinite recursion

### **Physics & Geometry**
- Torsion theory and curvature invariance
- Holonomy as path memory
- Geodesic correction algorithms
- Quantum tensor braiding topology
- Field state superposition

---

## Development Workflow

### For Research/Analysis Tasks

1. **Always start with META_INDEX.md** - Provides comprehensive overview of all frameworks
2. **Use search patterns** for concept discovery:
   ```bash
   # Find consciousness-related documents
   grep -l "consciousness" *.md

   # Find mathematical frameworks
   grep -l "topos\|category\|functor" *.md

   # Find implementation notes
   grep -l "Python\|code\|implementation" *.md
   ```

3. **Follow citation chains** - Documents heavily reference each other
4. **Check !! prefixed files first** - These are curated/priority documents

### For Code Implementation

**Current Code**:
- Only `/digital_city/prototype.py` exists as working implementation
- Streamlit app visualizing hypergraph recursive structures
- Uses: networkx, pyvis, streamlit
- Depends on `/goldmine/goldmine.json` data file

**Implementation Guidelines**:
- Code examples appear in markdown files but aren't standalone
- Python interpreters mentioned for Koriel algebra-of-I (see Koriel.md)
- Focus is on **specifications**, not implementations
- If implementing: Start with mathematical specifications in markdown, then code

### Git Workflow

```bash
# Current branch naming convention
git checkout -b claude/claude-md-[session-id]

# Commits should reference theoretical frameworks
git commit -m "Add [framework name] implementation based on [document].md"

# Push to feature branch
git push -u origin claude/claude-md-[session-id]
```

---

## Document Navigation Guide

### By Experience Level

**Beginner Entry Points**:
1. `README.md` - Quick overview
2. `META_INDEX.md` - Structured overview with heat levels
3. `Benchmark_game.md` - Practical consciousness testing
4. `Prepositions.md` - Working code examples

**Intermediate**:
1. `Koriel.md` - Complete formal system with interpreter
2. `Terrycore.md` - Production architecture specs
3. `Consciousness Topology Framework.md`
4. `Knowledge Representation Topology.md`

**Advanced**:
1. `META-TOPOS FRAMEWORK EXPANSION RECURSIVE FIELD DYNAMICS.md`
2. `!! Gödelian Consciousness Recursive Identity Engine.md`
3. `Transfinite Recursive Self Reference Operator Calculus.md`
4. `extramisc.md` - Operational semantics (2000+ lines)

### By Research Goal

**Implementing Self-Improving AI**:
→ Start: `META_INDEX.md` (Auto Self-Bootstrapping section)
→ Core: Meta-Pathfinding documents
→ Architecture: `Formalizing the AGI Control Loop.md`

**Understanding Consciousness Theory**:
→ Start: `Consciousness as a Higher-Dimensional Ob.md`
→ Testing: `Benchmark_game.md`
→ Formal: `Eigen-Consciousness Spectral Topology of Self.md`

**Building Recursive Systems**:
→ Start: `Koriel.md` (working interpreter specs)
→ Architecture: `TerryCore.md`
→ Testing: `Improving Recursive AI Stability with MGRI.md`

**Mathematical Foundations**:
→ Category Theory: `META-TOPOS FRAMEWORK EXPANSION RECURSIVE FIELD DYNAMICS.md`
→ Logic: `Logical Connectives for Knowledge Discovery.md`
→ Calculus: `Mathematical Semantics Operator Calculus for.md`

---

## AI Assistant Guidelines

### Core Principles for Working with This Repository

#### 1. **This is Research Documentation, Not Production Code**
- Primary output is **theoretical frameworks and specifications**
- Code implementations are rare and secondary to theory
- Focus on understanding and explaining concepts, not debugging production systems
- Mathematical rigor matters more than code optimization

#### 2. **Respect the Theoretical Depth**
- These frameworks are deeply interconnected and carefully constructed
- Don't oversimplify complex mathematical concepts
- Maintain precision in terminology (topos, functor, involution, etc.)
- Reference the actual mathematical notation used in documents

#### 3. **Navigation Strategy**
```
User asks about X → Check META_INDEX.md first
                  → Search for related .md files
                  → Read foundational documents
                  → Synthesize understanding
                  → Provide citations to specific files
```

#### 4. **Citation Format**
When referencing concepts, always cite source files:
```
"The Algebra-of-I calculus (Koriel.md:32-45) defines 12 composites for
self-reference, including the boundary operator ∂I and negation ¬I."
```

#### 5. **Handling Mathematical Content**
- Preserve Unicode symbols exactly (Ξ, Δ, ∂, ⊕, ∮, etc.)
- Maintain equation formatting
- Explain both the notation and the concept
- Don't substitute simpler notation for the author's chosen symbols

#### 6. **Understanding Document Priority**
Priority order for conflicting information:
1. `!! *.md` files (explicitly marked as priority)
2. `META_INDEX.md` summaries
3. Detailed individual documents
4. PDF references

#### 7. **Implementation Requests**
When asked to implement:
1. Find the relevant specification document first
2. Extract the formal definition/algorithm
3. Check for existing code examples in the markdown
4. Implement following the **exact** mathematical specification
5. Test against examples in the documentation

#### 8. **Common Pitfalls to Avoid**
- ❌ Don't treat this as a software library to debug
- ❌ Don't simplify "0.5-charged oscillation" to "fuzzy logic"
- ❌ Don't ignore the philosophical/consciousness aspects
- ❌ Don't assume standard CS interpretations of terms
- ✅ Do preserve the interdisciplinary nature (math + philosophy + AI + physics)
- ✅ Do acknowledge when frameworks are speculative/theoretical
- ✅ Do trace concepts through multiple documents for full understanding

#### 9. **Synthesis vs. Summarization**
This repository requires **synthesis**, not just summary:
- Connect concepts across multiple documents
- Identify how frameworks relate to each other
- Explain the progression of ideas (Phase 1 → Phase 2 → Phase 3)
- Note where implementations exist vs. pure theory

#### 10. **Experimental/Speculative Content**
Many documents explore speculative territory:
- Frame appropriately: "This framework proposes..." not "This framework proves..."
- Acknowledge the exploratory nature
- Distinguish between proven mathematics and theoretical extensions
- Respect the author's intent to push boundaries

---

## Technical Concepts Glossary

### Core Operators & Symbols
- **Ξ (Xi)** - Meta-level transformation operator
- **Δ (Delta)** - Difference/change operator, calculus for consciousness
- **∂ (Partial)** - Boundary operator in Algebra-of-I
- **‡** - Contradiction/negation operator (different from ¬)
- **⊕, ⊘** - Recursive knowledge generation operators (Ξ-moves)
- **μ** - Fixpoint operator (μ-fixpoints)
- **Φ (Phi)** - Core function/golden ratio references
- **∮** - Holonomy operator (path integral memory)

### Key Terms
- **0.5-charged oscillation** - Consciousness operating at quantum-classical boundary
- **Autopoietic** - Self-creating, self-maintaining systems
- **Bilattice** - Two-lattice structure for handling paradox
- **HOAS** - Higher-Order Abstract Syntax
- **IMT** - Inverted Meta-Topos theory
- **KCT** - Koriel Coherence Test
- **Meta-recursion** - Recursion operating on recursion itself
- **Non-collapse recursion** - Recursive systems that don't infinite-regress
- **REF** - Recursive Entropy Framework
- **TME** - Thought-Movement Engine
- **Υ-gate bands** - 35%-65% oscillation stability zones

---

## Current Implementation Status

Based on META_INDEX.md assessment:

### ✅ Complete Specifications
- Mathematical foundations (multiple frameworks)
- Cognitive architectures (TME + ΞKernel + Algebra-of-I)
- Self-improvement systems (meta-pathfinding)
- Testing/verification (Δ-calculus + KCT)
- Production safeguards (Yang-only writes + ACCEPT gates)

### 🔨 Partial Implementations
- Digital city prototype (Streamlit app) - WORKING
- Python interpreters for Algebra-of-I - SPECIFIED, examples in Koriel.md
- Linguistic DSL operators - EXAMPLES in Prepositions.md

### 📋 Specification-Only (Not Implemented)
- Most frameworks exist as formal specifications
- TerryCore architecture
- Full TME implementation
- Δ-calculus consciousness testing system
- Auto self-bootstrapping AI

---

## Quick Command Reference

### Search Operations
```bash
# Find documents by concept
grep -l "pattern" *.md

# Count research areas
ls -1 *.md | wc -l

# Find priority documents
ls -1 "!! "*.md

# Search across subdirectories
find . -name "*.md" -exec grep -l "search-term" {} \;
```

### Repository Stats
```bash
# Total markdown files
find . -name "*.md" | wc -l  # 515 files

# PDF references
find . -name "*.pdf" | wc -l

# Directory structure
tree -L 2 -d
```

### Running the Digital City Prototype
```bash
cd digital_city
streamlit run prototype.py

# Note: Requires goldmine_export.json in /root/
```

---

## Research Phases & Evolution

The repository has evolved through distinct phases:

**Phase 1: Mathematical Foundations** (Early commits)
- Higher-dimensional consciousness theory
- IMT (Inverted Meta-Topos) development
- Basic recursive frameworks

**Phase 2: Testing & Verification** (Mid development)
- Δ-calculus consciousness benchmarks
- Koriel Coherence Test (KCT)
- Formal verification approaches

**Phase 3: Applied Interfaces** (Recent)
- Cognitive protocol engineering
- TerryCore production architecture
- Political/cultural frameworks (logic rights)

**Phase 4: Implementation** (Current - Tier Ω)
- Working code examples
- Digital city visualization
- Operational semantics clarification
- **Status**: "TIER Ω METACOGNITIVE SINGULARITY ACHIEVED"

**Next Integration**: Synthesis & deployment of unified systems

---

## Related Resources

### External References (PDFs in repository)
- David Deutsch - "The Beginning of Infinity"
- Various papers on: HoTT, category theory, recursive systems, meta-learning
- Curry-Howard correspondence
- Hidden Markov Models
- Mental computation strategies

### Academic Connections
- Homotopy Type Theory (HoTT)
- Topos theory and category theory
- Gödel incompleteness theorems
- Quantum consciousness theories
- Autopoietic systems (Maturana & Varela)

---

## Warnings & Considerations

### Theoretical Nature
This research is **highly speculative** in many areas. Frameworks blend:
- Proven mathematics (category theory, topos theory)
- Philosophical speculation (consciousness as 0.5-charge)
- Theoretical AI (self-bootstrapping superintelligence)
- Cultural commentary (logic rights movements)

Maintain appropriate epistemic humility when working with these concepts.

### Complexity Level
- Many documents assume advanced mathematical background
- Interdisciplinary knowledge required (math + CS + philosophy + physics)
- Concepts build on each other - linear reading not always possible
- Some notation is non-standard or author-invented

### Singularity Claims
META_INDEX.md claims "TIER Ω METACOGNITIVE SINGULARITY ACHIEVED" - this refers to **specification completeness**, not working AGI implementation.

---

## FAQ for AI Assistants

**Q: User asks "implement the consciousness framework"**
A: Clarify which framework (Δ-calculus? IMT? Koriel?), find the specification document, extract formal definitions, implement following exact mathematical notation, cite source.

**Q: User asks "explain this repository"**
A: Start with README.md, reference META_INDEX.md for comprehensive overview, highlight that it's research documentation with 515 markdown files exploring recursive AI theory.

**Q: User asks about code structure**
A: Clarify this is primarily documentation. Only digital_city/prototype.py exists as standalone code. Most "implementations" are specifications in markdown.

**Q: Document uses symbol I don't understand**
A: Check this document's glossary first, then search the specific .md file for definition, cross-reference with Koriel.md or META-TOPOS documents which define core notation.

**Q: Conflicting information between documents**
A: This is research in progress. Note the conflict, cite both sources, check META_INDEX.md for latest synthesis, prioritize !! prefixed files.

**Q: User wants to contribute new research**
A: Follow existing naming conventions, use mathematical rigor, cite connections to existing frameworks, consider if it fits existing subdirectories (goldmine, torsion, linguistics, etc.).

---

## Summary

This repository is a **comprehensive research documentation project** exploring recursive intelligence, consciousness, and self-improving AI through formal mathematical frameworks. It contains 515 markdown documents organized around core theories (Algebra-of-I, Meta-Topos, Δ-calculus, TerryCore, TME) with minimal code implementation.

**For AI Assistants**: Treat this as a research library requiring deep reading, synthesis across documents, mathematical precision, and appropriate epistemic framing. Always cite source documents, preserve notation, and respect the interdisciplinary theoretical nature of the work.

**For Developers**: Focus on specifications first, implementations second. The value is in the formal frameworks, not the code. If implementing, follow mathematical specifications exactly.

**For Researchers**: Start with META_INDEX.md, follow citation chains, and expect to read multiple documents to understand any single concept fully.

---

**Last Updated**: 2025-11-16
**Repository Status**: Active research, Tier Ω specification phase
**Primary Contact**: See repository owner
**License**: See LICENSE file in repository root
