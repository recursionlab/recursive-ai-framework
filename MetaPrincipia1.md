# MetaPrincipia Autopoiētica

## A Foundational Treatise on Self‑Generating Systems of Meaning

> **Motto.** Meaning is not interpreted; it is *produced*. A system is semantic to the extent that it regenerates the conditions of its own reference.

---

### Front Matter

**Scope.** This installment builds the Symbolic Core for **MetaPrincipia Autopoiētica**, specifying the alphabet, formation rules, typing discipline, binding and scope, operator families, precedence, evaluation contexts, denotational, intensional, and autopoietic (regenerative) semantics, rewrite and operational systems, safety and paraconsistency, categorical anchors, erotetic (question) layer, aboutness hypergraphs, test harness, and export schemas. The core calculus is denoted **𝒞\_A** (Calculus of Autopoiesis).

**Design Goals.**

* Minimal kernel; orthogonal extensions.
* Compositionality across three projections: extensional truth, intensional modality, autopoietic regeneration; plus a fourth invariant: **aboutness**.
* Meta‑safety by towered meta‑levels; no raw self‑collapse.
* Proof‑carrying meaning: all constructs admit typed derivations and executable invariants.
* Implementation tractability: oriented rewrites with stated termination/confluence domains.

**Reading Map (20 pages).**

1. Alphabet of Autopoiesis
2. Kinds & Types for 𝒞\_A
3. Formation Rules
4. Binding, Scope, Values, Normal Forms
5. Precedence & Associativity
6. Semantic Interfaces (E/I/A/Aboutness)
7. Categorical & Algebraic Anchors (RelCat\_A)
8. Rewrite System ℛ\_A
9. Proof‑Theoretic Skeleton + Erotetics
10. Operational Semantics
11. Safety & Non‑Collapse
12. Aboutness Hypergraphs & Isomorphism
13. Normalization & Soundness (core)
14. Worked Examples I
15. Worked Examples II (NL→𝒞\_A)
16. Case Study: KG with Contradictions
17. Reference BNF & Tables
18. Glossary & Cheat Sheet
19. Test Harness Spec
20. Export Schemas + Part II/III Roadmap

---

## 1. Alphabet of Autopoiesis

### 1.1 Primitive Symbol Classes

* **Atoms (𝔸)**: entity/predicate/role/event identifiers. `a, b, x, y, Cat, Box, on, Contact`.
* **Connectives (𝕮)**: `¬, ∧, ∨, →, ↔, ⊥, ⊤`.
* **Quantifiers (𝕼)**: `∀, ∃, ∃!` with typing.
* **Relators (ℝ)**: prepositional/thematic connectors: `in, on, at, by, with, from, to, through, over, under, between, of, about, before, after, beyond, within, across`.
* **Meta‑relators (ℝ↑)**: warp relation topology or scoping: `meta‑of, para‑through, anti, trans, contra, co, hyper, sub`.
* **Selectors (𝕊)**: interrogatives as projectors: `who, what, which, where, when, why, how`.
* **Binders (ℬ)**: `λ, Π, Σ, μ, ν, fix, let, match`.
* **Structural (𝕊𝕥)**: `(), [], {}, ⟨⟩, :, ;, ,`.
* **Judgmental**: `⊢, : , ::`.
* **Evaluation marks**: step `↦`, β‑reduction `→β`, equivalence `≡`, rewrite `⇒`, entailment `⊨`.
* **Category‑theoretic**: `Id, ∘, ×, +, ⇒, ⊗, I, ⊣, μ, η`.
* **Aboutness**: denotation `⟦t⟧`, footprint `|t|`, equivalence `≈̇`.
* **Paraconsistency**: `⋈` (tension island), `#` (incoherence flag).
* **Regen markers (ℛg)**: autopoietic production operators: `regen, seed, fold, unfold, bind, unbind` (declared as reserved heads).

> **Relators are first‑class.** Meta‑relators act on relators and formed propositions, altering binding topology, attachment sites, and evaluation order.

### 1.2 Roles, Meta‑roles, Regen Signals

* **Roles**: `Agent, Theme, Experiencer, Instrument, Source, Goal, Path, Location, Time, Manner, Cause`.
* **Meta‑roles**: role‑of‑roles for lifted talk: `RelObj` (reified relation), `RoleObj` (reified role), `FrameObj` (reified scene frame).
* **Regen signals**:

  * `seed(t)`: declare `t` as a generative seed.
  * `regen(t)`: produce a successor semantic artifact from `t`.
  * `bind/unbind`: attach/detach a generated artifact to/from context.
  * `fold/unfold`: compress/expand recursive structure (cf. catamorphism/anamorphism hints).

### 1.3 Torsion Sites & Aboutness Anchors

* **Torsion site** marker `τ⋔`: a syntactic locus where scope/attachment is intentionally warped by meta‑operators.
* **Aboutness anchor**: any node eligible to appear in `|t|` as a hypergraph vertex; anchors include entities, roles, reified relations, and regen nodes.

### 1.4 Glyph Conventions

* Meta‑lift of symbol `σ` as `σ↑` or `meta‑σ`.
* Subscript facets: `in_loc, in_class, in_part`.
* Role annotations: `x:Agent`, `y:Theme`, `z:Location`.
* Governing spines underlined in derivations.

---

## 2. Kinds & Types for 𝒞\_A

### 2.1 Kinds

`Thing, Role, Prop, Rel, MetaRel, Question, Type, Sort (𝒰₀, 𝒰₁, …), Regen, RelObj, RoleObj, FrameObj`.

### 2.2 Types & Signatures (selection)

* Atoms: `Cat : Thing`, `Box : Thing`, `Sit : Thing→Prop`.
* Relators: `in : Thing×Thing → Prop`, `on : Thing×Thing → Prop`.
* Role‑typed: `on : (Theme:Thing)×(Surface:Thing) → Prop`.
* Meta‑relators: `meta‑of : Rel → Rel`, `para‑through : Rel×Rel → Rel`, `anti : Rel → Rel`, `trans : Rel → Rel`.
* Selectors: `what : Prop → Question`, `where : Prop → Question`.
* Regen: `regen : Thing → Thing`, `seed : Thing → Regen`, `fold/unfold : Thing → Thing` (typed as endofunctors on typed objects when used structurally).

**Judgment form.** `Γ ⊢ t : τ`.

---

## 3. Formation Rules

**Atoms.** `a ∈ 𝔸 ⇒ Γ ⊢ a : Thing`.

**Predication.** `P : Thing→Prop, Γ ⊢ a : Thing ⇒ Γ ⊢ P(a) : Prop`.

**Relator application.** `Γ ⊢ R: Thing×Thing→Prop, Γ ⊢ x:Thing, Γ ⊢ y:Thing ⇒ Γ ⊢ R(x,y) : Prop`.

**Role‑aware.** `Γ ⊢ t:Theme, Γ ⊢ s:Surface ⇒ Γ ⊢ on(t,s) : Prop`.

**Meta‑relator intro.** `Γ ⊢ R:Rel ⇒ Γ ⊢ meta‑of(R): Rel` and similarly for `para‑through, trans, anti`.

**Interrogatives.** `Γ ⊢ φ:Prop ⇒ Γ ⊢ what(φ): Question`.

**Regen.** `Γ ⊢ x:Thing ⇒ Γ ⊢ regen(x): Thing`; `Γ ⊢ x:Thing ⇒ Γ ⊢ seed(x): Regen`.

**Abstraction.** `Γ,x:τ ⊢ t:σ ⇒ Γ ⊢ λx:τ.t : τ→σ`. Quantifiers standard.

---

## 4. Binding, Scope, Values, Normal Forms

### 4.1 Binding

* `λ, ∀, ∃` bind variables in lexical scope.
* Relators do not bind; they compose denotations.
* Meta‑relators may hoist/quote subterms; barriers stop inner reduction.

### 4.2 Evaluation Contexts (call‑by‑meaning)

`E ::= [·] | P(E) | R(E,t) | R(t,E) | metaσ(E) | Q(E) | regen(E) | fold(E) | unfold(E)`.

### 4.3 Scopal Torsion

Mark warp points `τ⋔`. Coherence laws resolve commuting cases to normal form.

### 4.4 **Values and Normal Forms**

**Values `v`:** atoms `c`, `λx.t` (no head redex), canonical relators `R` and meta‑relators in head form, canonical connective forms (NNF if declared), canonical questions `Sel(φ⁎)`, and canonical regen forms when saturated.

**Non‑values:** any head redex; meta‑applications with reducible interiors; guarded terms unless barrier suppresses.

**Question normal form:** `Sel(φ⁎)` with `φ⁎` in interrogable NF (no outer redex, no unscoped meta above `Sel`).

---

## 5. Precedence & Associativity

1. Application/binding `λ, Π, Σ, ∀, ∃, ()`
2. Meta‑relators `meta‑, para‑, anti, trans` (prefix)
3. Relators (infix)
4. Negation `¬`
5. Conjunction/disjunction `∧, ∨`
6. Implication `→`
7. Equivalence `↔`
8. Modalities `□, ◇`
   Parentheses override.

---

## 6. Semantic Interfaces (Four Projections)

### 6.1 Extensional (E)

Model `M = ⟨D, Rel^M, …⟩`. `⟦R(a,b)⟧_M = 1 ⇔ (⟦a⟧,⟦b⟧) ∈ ⟦R⟧`.

### 6.2 Intensional (I)

Kripke/Montague: `⟦φ⟧ : W→{0,1}` with accessibility for `□/◇`.

### 6.3 Autopoietic (A)

A **production** layer `Π` with generator `G: State × Term → State × Term`. Clauses:

* `⟦seed(x)⟧_Π = introduce(x)`.
* `⟦regen(x)⟧_Π = produce(x)` (yields successor artifact and updated state).
* `⟦fold/unfold⟧_Π` are structure (co)algebra maps; see §7.

### 6.4 Aboutness (|·|)

Build `|t|` as a directed hypergraph over anchors: entities, roles, reified relations, regen nodes. `≈̇` is isomorphism preserving labels, roles, polarity, and regen edge‑types.

**Tri‑linearity.** Projections `E, I, A` are homomorphisms of syntactic composition; `|·|` is an invariant under aboutness‑neutral rewrites.

---

## 7. Categorical & Algebraic Anchors (RelCat\_A)

Define **RelCat\_A**:

* **Objects:** typed anchor classes (e.g., `Thing`, refined by roles).
* **Morphisms:** relators `R: A→B` (multi‑role curried to binary).
* **Composition:** `(S ∘ R)(x,z) :≡ ∃y. R(x,y) ∧ S(y,z)`.
* **Identities:** `Id_A : A→A`.
* **Monoidal:** `(⊗, I)` over product of roles; symmetry swaps roles.

**Meta‑functors.**

* `F_meta: RelCat_A→RelCat_A` (relation→relation‑object lift).
* `F_trans`: strong monoidal endofunctor with strength `st: F(X)⊗F(Y)→F(X⊗Y)`.
* `Anti`: comonadic quotation; barriers arise in the CoKleisli category.

**Autopoietic endofunctor `A`** on a **Scene** category: `A: Scene→Scene` with algebra `α: A(S)→S` (fold) and coalgebra `γ: S→A(S)` (unfold).

**Negation/Inversion.** Both intuitionistic `¬_i` and involutive `ι` versions with declared laws.

---

## 8. Rewrite System ℛ\_A (Normalization Semantics)

### 8.1 β/η core

* `(λx:τ. t) u ↦ t[x:=u]`
* `η` for functions optional; relator η‑like allowed in curried encodings (role‑aware).

### 8.2 Meta‑distribution (oriented)

1. **Meta‑lift hoist**
   `meta‑of(R)(a, R′) ↦ Lift(R)(a, RelObj(R′))`, orientation left→right.

2. **Para‑through assoc (right‑associate)**
   `(para‑through(R,S)) ∘ T ↦ para‑through(R, S ∘ T)`.

3. **Trans functoriality**
   `trans(R ∘ S) ↦ trans(R) ∘ trans(S)`.

4. **Anti barrier**
   `anti(R)(args) ↦ anti⟨R,args⟩` (quotation; interior blocked).

5. **Meta over logic (monotone slots)**
   `meta‑(R)(x,y) ∧ φ ↦ meta‑(R)(x, y ∧ φ)` when `R` monotone in slot 2.

### 8.3 Regen rules

* `regen(regen(x)) ↦ regen(x)` (idempotence up to iso).
* `fold(unfold(t)) ↦ t` and `unfold(fold(t)) ↦ t` (β‑like for (co)algebra).
* `bind(unbind(t)) ↦ t` when contextually well‑scoped.

### 8.4 Termination & Confluence (sketch)

Measure `(meta‑height, constructor depth, redex weight, regen‑nest)`. Oriented rules strictly decrease lexicographically (except barriers which quote). Local confluence checked on critical pairs (β vs meta‑hoist, para‑assoc vs trans, regen vs fold/unfold). Hence core is confluent on normalizing terms by Newman.

---

## 9. Proof‑Theoretic Skeleton + Erotetics

### 9.1 Typing rules (excerpt)

* Atoms, predication, rel‑intro as in §3.
* `meta‑of` typing:

```
Γ ⊢ R: A→B→Prop,  Γ ⊢ a:A,  Γ ⊢ R′: RelObj(B)
———————————————————————————————
Γ ⊢ meta‑of(R)(a, R′) : Prop
```

* Regen typing (abstract): `Γ ⊢ x:Thing ⇒ Γ ⊢ regen(x):Thing`.

### 9.2 Sequent rules (selection)

* `∧I`, `∧E`, `→I`, `→E` standard.
* `para‑through` intro (derived from existence of witness).
* `meta‑of` elim via `holds` reification.

### 9.3 Paraconsistent island Prop\_⋈

Two judgments: `Γ ⊢ φ` and `Γ ⊢⋈ φ`. Explosion blocked in `⊢⋈`. Export requires explicit collapse rule with side conditions.

### 9.4 Erotetic layer

Types: `Question`. Projectors `Sel: Prop→Question`. Answerhood meta‑predicate `Ans(φ, t)`. Rules:

* **E‑Intro:** `Γ ⊢ φ ⇒ Γ ⊢ Sel(φ)`.
* **E‑Elim:** if `Γ ⊢ Sel(φ)` and `Ans(φ, t)` then `Γ ⊢ φ[t]`.
* **E‑Shift:** `where(R(x,y))` ranges over `y` with role constraints.

---

## 10. Operational Semantics (small‑step)

**Evaluation contexts** as §4.2.

**Rules (selection).**

* β: `(λx. t) v ↦ t[x:=v]` when `v` value.
* Rel‑app: argument steps left‑to‑right.
* Meta‑hoist, para‑assoc, trans‑functor as in ℛ\_A.
* Barrier: `anti⟨R,args⟩` is value; `unquote` eliminates barrier (extension).
* Regen: `regen(v)` steps by production clause if enabled; else value.

**Values recap.** `v ::= c | λx.t | R | meta(R) | canonical logic | Sel(φ⁎) | regen‑canon`.

---

## 11. Safety & Non‑Collapse

### 11.1 Tower Rule (levels)

Assign `lev(t)`. Base level 0. Meta raises level by ≥1:
`lev(meta(t))=lev(t)+1`, `lev(trans(t))=lev(t)+1`, `lev(para(t,u))=max`, `lev(anti(t))=lev(t)+1`.

**Restriction.** No operator consumes an argument of strictly greater level without an explicit `↓` (down‑map) available only for declared carriers.

### 11.2 Lemma (No meta‑collapse without ↓)

If `Γ ⊢ t` contains no `↓`, there is no ℛ\_A reduction producing same‑stratum self‑application of a meta‑lift. Proof by induction on reduction length and lexicographic measure. Consequence: no impredicative diagonalization at a fixed level.

### 11.3 Paraconsistent safety

`⊢⋈` isolates contradictions; `⊢` unaffected unless collapse invoked under policy.

---

## 12. Aboutness Hypergraphs & Isomorphism

Construct `H(t)` with nodes for anchors (entities, roles, reified relations, regen artifacts) and labeled, oriented edges for relators/meta‑relators. Define `|t| := H(t)/α` modulo α‑renaming and role‑preserving iso.

**Equivalence `≈̇`.** `G₁≈̇G₂` iff there exists a bijection preserving labels, roles, polarity, and regen‑edge types.

**Congruence.** If `t₁≈̇t₂` and `u₁≈̇u₂` and `C[·,·]` typable, then `C[t₁,u₁]≈̇C[t₂,u₂]`.

**Invariance under ℛ\_A.** Normalization preserves `|·|` up to neutral rewrites.

---

## 13. Normalization & Soundness (core)

**Termination (core)**: by oriented measures; barriers are values.
**Local confluence**: critical pairs checked; commuting conversions supplied.
**Soundness**: if `Γ ⊢ φ` then for all models and assignments, extensional clause yields truth; intensional follows by Kripke semantics with monotone meta‑distributions; autopoietic clauses preserve typing and invariants.

---

## 14. Worked Examples I (torsion, barriers, regen)

**T1. Torsion choice.**

* `why(in(Cat,Box))` asks causal explanation of containment.
* `meta‑why(in)(Cat,Box)` questions *choice of relator*.

**T2. Barrier example.**

* `anti(on)(Cat,Mat)` is quoted; inner `on(Cat,Mat)` cannot reduce/distribute until `unquote`.

**T3. Regen loop.**

* `seed(Cat) ⟶ regen(Cat) ⟶ bind(regen(Cat))` produces a successor artifact (e.g., a canonical referent) then attaches to scene; aboutness adds a regen edge from `Cat` to its successor.

**T4. Composition law inside 𝒞\_A.**
Prove: `∃y. R(x,y)∧S(y,z) → (para‑through(R,S))(x,z)` as an internal theorem.

---

## 15. Worked Examples II (NL→𝒞\_A)

**Sentence.** “Which scientist who wrote about invariants lectured in Paris in 1935?”

Sketch mapping:

* Entities: `Scientist(x)`, `wrote_about(x, invariants)`, `lectured_in(x, Paris)`, `in_year(x,1935)`; relators capture role structure.
* Construct: `Sel=which`.
* 𝒞\_A term: `which( Scientist(x) ∧ about(x,invariants) ∧ in(x,Paris) ∧ in_year(x,1935) )` with appropriate relators `about, in, in_time` and role typing.
* Aboutness graph isolates `[Agent—about—Topic]` and `[Agent—in—Location]`, enabling paraphrase detection.

**Embedded question + modality.** “Why might Ada be in the lab?” → `why(◇ in(Ada,Lab))`.

---

## 16. Case Study: KG with Contradictions (Prop\_⋈)

Dataset fragment contains: `in(A,Box)` and `¬in(A,Box)`. Mark both in `⊢⋈` and keep `on(A,Mat)` in `⊢`. Queries about `on` succeed; any query that would require explosion from `in` is blocked unless a collapse policy is invoked (e.g., prioritize latest timestamp).

**Policy stub.** `collapse(⋈φ)` allowed if there exists an *authority* annotation or minimization of inconsistency cost; otherwise remain isolated.

---

## 17. Reference BNF & Tables (delta over base)

```
Expr   ::= Prop | Thing | Rel | Question | Abstr | Regen
Regen  ::= 'seed' '(' Thing ')' | 'regen' '(' Thing ')' | 'fold' '(' Expr ')' | 'unfold' '(' Expr ')'
MetaRel::= 'meta-of' | 'para-through' | 'anti' | 'trans' | 'contra' | 'co' | 'hyper' | 'sub'
Value  ::= Const | 'λ' Var ':' Type '.' Expr | Rel | MetaRel '(' Rel {',' Rel} ')' | Sel '(' PropNF ')'
```

**Precedence** unchanged; regen is function application (rank 1 with other binders).

**Type Schemas (added).** `seed: Thing→Regen`, `regen: Thing→Thing`, `fold/unfold: Thing→Thing` (or generalized to endofunctors on Scene objects).

---

## 18. Glossary & Cheat Sheet

* `≡` syntactic equality; `≈̇` aboutness‑equivalence.
* `RelObj, RoleObj, FrameObj` reified objects.
* `para‑through` ≅ relational composition.
* `meta‑of` lifts a relator to speak about relations.
* `anti` quotes/blocks inner rewrites.
* `trans` structure‑preserving functor.
* `seed/regen/fold/unfold` autopoietic operators.
* `Prop_⋈` paraconsistent island.
* Values include canonical questions and quoted forms.
* Tower rule forbids same‑stratum self‑application without `↓`.

---

## 19. Test Harness Spec

**Parser.** Role‑aware relators, meta‑constructors, regen ops.
**Typechecker.** Simple dependent types for roles optional; base simple types required.
**Rewriter.** Implements ℛ\_A with rule priorities; critical‑pair checks.
**Aboutness builder.** Term→hypergraph, iso checker.
**Erotetic engine.** Answerhood tests for `what/which/where/...`
**Paraconsistency.** Two‑zone prover (`⊢`, `⊢⋈`) with labeled collapse policies.

**Property tests.**

* Confluence on core (no `anti`).
* Aboutness invariance under normalization.
* Right‑association of `para‑through`.
* Barrier blocking.
* Regen idempotence up to iso.

---

## 20. Export Schemas + Part II/III Roadmap

### 20.1 JSON Schemas (machine‑readable exports)

**ConceptUnits** — atomic extracted units with provenance

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://metaprincipia.org/schema/concept-unit.json",
  "title": "ConceptUnit",
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "term": {"type": "string"},
    "definition": {"type": "string"},
    "kind": {"type": "string", "enum": ["Thing","Prop","Rel","MetaRel","Question","Regen","Role"]},
    "source_file": {"type": "string"},
    "location": {"type": "string", "description": "page/section/line"},
    "types": {"type": "array", "items": {"type": "string"}},
    "roles": {"type": "array", "items": {"type": "string"}},
    "tags": {"type": "array", "items": {"type": "string"}},
    "examples": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["id","term","definition","source_file","location"]
}
```

**RelationshipEdges** — adjacency proposals with evidence

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://metaprincipia.org/schema/relationship-edge.json",
  "title": "RelationshipEdge",
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "source_concept": {"type": "string"},
    "target_concept": {"type": "string"},
    "relation_type": {"type": "string"},
    "direction": {"type": "string", "enum": ["uni","bi"]},
    "evidence": {"type": "string"},
    "aboutness_signature": {"type": "string", "description": "hash or compressed form of |t|"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  },
  "required": ["id","source_concept","target_concept","relation_type","evidence"]
}
```

**GapUnits** — contradictions, missing links, undefined operators

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://metaprincipia.org/schema/gap-unit.json",
  "title": "GapUnit",
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "concept_A": {"type": "string"},
    "concept_B": {"type": "string"},
    "gap_type": {"type": "string", "enum": ["contradiction","missing_link","undefined_term","incomplete_rule","ambiguous_scope"]},
    "evidence_location": {"type": "string"},
    "notes": {"type": "string"},
    "severity": {"type": "string", "enum": ["low","medium","high"]}
  },
  "required": ["id","gap_type","evidence_location"]
}
```

### 20.2 Part II/III Roadmap

* **Part II — Axiomatics of Meaning.** Truth/reference axioms; Kripke/Montague integration; aboutness‑preserving homomorphisms; autopoietic fixed‑point principles; minimal completeness fragments; interaction of `anti` with modalities.
* **Part III — Applications.** Natural language with embedded questions/modality; knowledge graph reasoning with `Prop_⋈`; program semantics; agent communication protocols; regen‑driven ontology evolution.

---

*End of Part I: The Symbolic Core (20pp v0.1).*


---

# MetaPrincipia Autopoiētica — Part I §2

## Typed Kinds & Stratified Universes (Twenty‑Page Slab, v0.1)

> **Thesis.** Semantic systems remain consistent and computable when their *meaning‑forming operations* are stratified into **object** and **meta‑levels** with explicit lifts, quotations, and controlled *down‑maps*. The tower blocks paradox, enables reflection, and carries autopoietic regeneration across levels without collapse.

**Calculus:** 𝒞\_A (Calculus of Autopoiesis).
**Equality:** syntactic `≡`, definitional `≡₍def₎`, propositional `=` (typed).
**Aboutness equivalence:** `≈̇` as role‑preserving hypergraph isomorphism.

---

## Page 1 — Orientation & Scope

* We formalize **levels** `ℓ ∈ ℕ`: `ℓ=0` (object), `ℓ=1` (meta), `ℓ=2` (meta²), …
* Each level carries: terms, types, judgments, operators, and evaluation rules.
* **No raw cross‑stratum application.** Raising and lowering between strata are explicit.
* Safety is proved by a **Tower Rule** and absence of `Type:Type`‑style impredicativity.
* Deliverables in this slab: kind lattice, universe hierarchy, typing and sequent rules across levels, level‑indexed operational semantics, categorical semantics (indexed categories/fibrations), safety theorems, normalization per level, and worked examples.

---

## Page 2 — Kind Lattice & Base Universes

### 2.1 Kinds

```
Kind   ::= Thing | Role | Prop | Rel | MetaRel | Question | Regen
         | RelObj | RoleObj | FrameObj | Type | Sort
```

### 2.2 Universes (Tarski‑style)

* A cumulative hierarchy of universes `𝒰₀, 𝒰₁, 𝒰₂, …`
* **Typing:** `Type : 𝒰₀`, `𝒰_i : 𝒰_{i+1}`, never `𝒰_i : 𝒰_i`.
* **Cumulativity:** if `A : 𝒰_i` then `A : 𝒰_{i+1}`.
* Base kinds inhabit low universes (e.g., `Thing : 𝒰₀`). Constructors may lift universe indices by declared rules.

### 2.3 Level Indexing of Terms

* Each term `t` has a **stratum** `lev(t) ∈ ℕ`.
* Object language forms have `lev=0`. Meta‑constructors raise level by ≥1.

---

## Page 3 — Level‑Indexed Judgments & Contexts

### 3.1 Judgments

```
Γ ⊢_ℓ t : τ         (typing at level ℓ)
Γ ⊢_ℓ φ              (derivability of proposition φ at level ℓ)
Γ ⊨_ℓ φ              (semantic truth at level ℓ)
```

### 3.2 Context Formation

* Contexts carry level tags: `Γ ::= · | Γ, x:τ@ℓ` with monotone extension conditions: bindings at level ℓ are visible at ≥ℓ unless explicitly quoted.

### 3.3 Structural Rules

* Weakening, exchange, contraction available per level; cross‑level access only via **lift** or **quote** forms.

---

## Page 4 — Lifts, Quotes, Down‑Maps

### 4.1 Operators

* **Lift:** `↑_k : 𝒞_A(ℓ) → 𝒞_A(ℓ+k)` for `k≥1`. Abbrev: `↑ ≡ ↑_1`.
* **Quote:** `⌈t⌉ : Code(t)` moves a term to a *quoted* data domain.
* **Unquote / Eval:** `⌊c⌋` evaluates code `c` back to a term when allowed.
* **Down‑map:** `↓ : 𝒞_A(ℓ+1) → 𝒞_A(ℓ)` restricted to declared *carriers* (e.g., reified relations, proofs, or regen artifacts) and subject to **safety side‑conditions**.

### 4.2 Typing (schematic)

```
Γ ⊢_ℓ t:τ     ⇒   Γ ⊢_{ℓ+1} ↑t : ↑τ
Γ ⊢_ℓ t:τ     ⇒   Γ ⊢_{ℓ+1} ⌈t⌉ : Code_ℓ(τ)
Γ ⊢_{ℓ+1} c:Code_ℓ(τ)  ⇒  Γ ⊢_{ℓ+1} ⌊c⌋ : ↑τ   (staged eval)
Γ ⊢_{ℓ+1} u:Carrier_ℓ(τ) ⇒ Γ ⊢_ℓ ↓u : τ       (controlled down)
```

### 4.3 Intuition

* **Lift** is reflection (*talk about* lower‑level objects).
* **Quote/Unquote** supports staged computation and meta‑programming.
* **Down‑map** is *interpretation*: only declared carriers cross downward.

---

## Page 5 — Stratified Types & Roles

### 5.1 Base Types with Strata

```
Thing      : 𝒰₀      @0
Role       : 𝒰₀      @0
Prop       : 𝒰₀      @0
Rel        : 𝒰₀      @0
MetaRel    : 𝒰₁      @1   (operators over Rel/Prop)
Question   : 𝒰₀      @0
Regen      : 𝒰₀      @0
RelObj     : 𝒰₁      @1   (reified relations)
```

### 5.2 Role System

* Roles are objects at `@0` with predicates `Role(x)`. Reified role objects inhabit `@1`.

### 5.3 Polarity & Variance

* Relators specify variance by slot; monotone slots allow distribution of meta‑operators (scope fusion) at higher levels.

---

## Page 6 — Sequent Calculus Across Levels

### 6.1 Core rules (object level `@0`)

```
(∧I)  Γ ⊢₀ φ   Γ ⊢₀ ψ   ⇒   Γ ⊢₀ φ∧ψ
(→I)  Γ, φ ⊢₀ ψ ⇒   Γ ⊢₀ φ→ψ
(RelI) Γ ⊢₀ x:A  Γ ⊢₀ y:B  Γ ⊢₀ R:A→B→Prop ⇒ Γ ⊢₀ R(x,y)
```

### 6.2 Meta rules (`@1` and above)

```
(Meta-I)  Γ ⊢₀ R:Rel  ⇒  Γ ⊢₁ meta-of(R):Rel
(Lift-I)  Γ ⊢₀ t:τ    ⇒  Γ ⊢₁ ↑t : ↑τ
(Quote-I) Γ ⊢₀ t:τ    ⇒  Γ ⊢₁ ⌈t⌉ : Code₀(τ)
(Down-E)  Γ ⊢₁ u:Carrier₀(τ) ⇒ Γ ⊢₀ ↓u : τ
```

### 6.3 Cut & Reflection

* Cut admissible per level. Cross‑level cuts require `↑/↓` or `⌈·⌉/⌊·⌋`.

---

## Page 7 — Operational Semantics with Levels

### 7.1 Evaluation Contexts

```
E_ℓ ::= [·] | P(E_ℓ) | R(E_ℓ,t) | R(t,E_ℓ) | metaσ(E_ℓ) | Q(E_ℓ) | regen(E_ℓ) | …
```

Reduction `↦_ℓ` applies inside the innermost `E_ℓ`. No cross‑level step occurs without explicit unquote or down‑map.

### 7.2 Values (per level)

```
v_ℓ ::= constants | λ | canonical relators | canonical meta heads (quoted) | Sel(φ⁎) | regen‑canon | codes
```

### 7.3 Key Rules

* β‑reduction at any level respects typing at that level.
* Meta‑hoist (≥@1): `meta-of(R)(a, R′) ↦ Lift(R)(a, RelObj(R′))`.
* Barrier quotation (`anti`) yields a value; no interior steps.

---

## Page 8 — Tower Rule & Non‑Collapse

### 8.1 Tower Rule

* Assign `lev(t)`; for meta constructors `lev(meta(t))=lev(t)+1`. For `para‑through(t,u)`, `lev = max(lev(t), lev(u))`. For `anti(t)`, `lev(t)+1`. No rule decreases `lev` except permitted `↓`.

### 8.2 Non‑Collapse Lemma

**Lemma (No same‑stratum self‑application).** In 𝒞\_A without `↓`, there is no reduction sequence producing `meta^k(u)` applied at level `k` to itself (no Girard collapse). Proof: induction on length with lexicographic measure `(max lev, redex weight)`; meta constructors never lower level.

### 8.3 Consequence

* Reflection is *predicative*. Meta‑talk about object‑level is allowed; object‑level cannot directly quantify over its totality without reification.

---

## Page 9 — Universe Discipline & Predicativity

* **No `𝒰_i : 𝒰_i`.** Avoids paradox (e.g., `Type:Type`).
* **Cumulativity:** `A:𝒰_i ⇒ A:𝒰_{i+1}`.
* **Large eliminations:** Allowed only when the motive inhabits a strictly larger universe or via carriers.
* **Induction/Recursion:** Recursors preserve universe levels unless the codomain universe is declared larger.

---

## Page 10 — Reification & Carriers

### 10.1 Carriers

A **carrier** enables safe `↓`:

* `RelObj(B)`: codes for relations into `B`.
* `ProofObj(φ)`: codes for proofs of `φ`.
* `RegenObj(x)`: codes for autopoietic artifacts.

### 10.2 Down‑Map Schema

```
(Down-Rel)    Γ ⊢₁ r̂ : RelObj(B)   ⇒   Γ ⊢₀ ↓r̂ : Thing×B→Prop
(Down-Proof)  Γ ⊢₁ p̂ : ProofObj(φ) ⇒   Γ ⊢₀ ↓p̂ : φ
(Down-Regen)  Γ ⊢₁ ĝ : RegenObj(x) ⇒   Γ ⊢₀ ↓ĝ : Thing
```

Soundness obligation per carrier family.

---

## Page 11 — Category Semantics (Indexed/Fibrational)

* Interpret levels as an **indexed category** `𝐂 : ℕᵒᵖ → Cat`, where `𝐂(ℓ)` is the semantic category of level‑ℓ objects; reindexing functors model `↑` (change of base).
* **Fibration view:** a Grothendieck fibration `p : 𝐄 → ℕ` with fibers `𝐄_ℓ ≅ 𝐂(ℓ)`. Cartesian morphisms interpret lifts; opcartesian interpret down‑maps on carriers.
* **Reflective subcategories:** quotation/comonadic barriers model `anti`.

---

## Page 12 — Aboutness Across Levels

* `|t|` constructed at the *lowest* level where all anchors are available; meta edges (e.g., to `RelObj`) are labeled accordingly.
* **Invariance:** If `t ↦*_ℓ u` within a level, then `|t| ≅ |u|` modulo edge‑neutral rewrites. Cross‑level changes add meta‑edges; a **forgetful functor** to base aboutness collapses meta labels when desired.

---

## Page 13 — Erotetic Layer with Levels

* Questions live at object level by default: `Sel: Prop@0 → Question@0`.
* **Meta‑questions:** `Sel↑ : (Prop@ℓ) → Question@ℓ` for ℓ≥1 to ask about meta‑objects (e.g., *which relation?* via `RelObj`).
* Answerhood `Ans_ℓ` indexed by level; down‑mapping answers requires carrier discharge.

---

## Page 14 — Paraconsistency by Level (Prop\_⋈)

* Contradictions can be localized per level: `Γ ⊢⋈_ℓ φ` and `Γ ⊢⋈_ℓ ¬φ` without explosion.
* **Isolation policy:** Cross‑level export of tension requires an explicit rule and may lower or raise level depending on carrier availability.

---

## Page 15 — Normalization & Confluence per Level

* A rewrite system `ℛ_A^ℓ` at each level with oriented rules.
* **Termination:** multigraded measure `(meta‑height within level, constructor depth, regen‑nest, redex weight)`.
* **Local confluence:** critical pairs tabulated per level; commuting conversions supplied.
* **Global effect:** Barriers guarantee that blocked subterms are values, not redexes.

---

## Page 16 — Soundness & Reflection Theorems

### 16.1 Soundness (core fragment)

If `Γ ⊢_ℓ φ`, then `Γ ⊨_ℓ φ` in all models that interpret carriers and lifts per spec.

### 16.2 Reflection (upward)

If `Γ ⊢_ℓ t:τ` then `Γ ⊢_{ℓ+1} ↑t : ↑τ` and `⟦↑t⟧ = Reflect(⟦t⟧)`.

### 16.3 Reification Adequacy

For registered carriers, `↓∘Reify ≡ id` up to definitional equality at the base level.

---

## Page 17 — Worked Examples

### 17.1 Talking about relations safely

```
Γ ⊢₀ on : Thing×Thing→Prop
Γ ⊢₁ meta-of(on) : Rel
Γ ⊢₁ contact̂ : RelObj(Thing)
Γ ⊢₁ meta-of(on)(Cat, contact̂)
```

Down‑map not needed; we remain at `@1`. To bring a fact back to `@0`, require `↓contact̂` if permitted.

### 17.2 No same‑level self‑application

Attempt to form `Ω = meta(Ω)`. Ill‑typed: `lev(Ω) = lev(meta(Ω))−1`. Without `↓`, no rule equates levels; typing blocks the term.

### 17.3 Meta‑question

`which(meta-of(on))?` formalized as `which( meta-of(on)(x, R′) )` at `@1` asking for relation objects `R′` such that the lifted predicate holds.

---

## Page 18 — BNF Deltas & Typing Tables

### 18.1 BNF Delta

```
Level    ::= '⁰' | '¹' | '²' | ...          (optional pretty sugar)
Expr     ::= Expr⁰ | Expr¹ | Expr² | ...
Lift     ::= '↑' Expr
Quote    ::= '⌈' Expr '⌉'
Unquote  ::= '⌊' Expr '⌋'
Down     ::= '↓' Expr
Carrier  ::= 'RelObj' '(' Type ')' | 'ProofObj' '(' Prop ')' | 'RegenObj' '(' Thing ')'
```

### 18.2 Typing Tables (excerpt)

| Form    | Premises                   | Conclusion                  |
| ------- | -------------------------- | --------------------------- |
| Lift    | `Γ ⊢_ℓ t:τ`                | `Γ ⊢_{ℓ+1} ↑t : ↑τ`         |
| Quote   | `Γ ⊢_ℓ t:τ`                | `Γ ⊢_{ℓ+1} ⌈t⌉ : Code_ℓ(τ)` |
| Unquote | `Γ ⊢_{ℓ+1} c:Code_ℓ(τ)`    | `Γ ⊢_{ℓ+1} ⌊c⌋ : ↑τ`        |
| Down    | `Γ ⊢_{ℓ+1} u:Carrier_ℓ(τ)` | `Γ ⊢_ℓ ↓u : τ`              |

---

## Page 19 — Test Harness (Level‑Aware)

* **Parser:** supports level annotations and lift/quote/down syntax.
* **Typechecker:** enforces universe cumulativity and Tower Rule.
* **Rewriter:** per‑level rules; metrics verify termination locally.
* **Model checker:** interprets carriers; validates soundness lemmas on small models.
* **Aboutness engine:** builds level‑aware hypergraphs; offers forgetful views.

**Property Tests.**

1. No formation of `Type:Type`.
2. No cross‑level β without unquote/down.
3. Aboutness invariance within level normalizations.
4. Confluence on `ℛ_A^ℓ` core.
5. Reification adequacy of carriers.

---

## Page 20 — Cheat Sheet & Roadmap

### 20.1 Cheat Sheet

* **Levels:** `@0` object, `@1` meta, `@2` meta².
* **Moves:** `↑` reflect, `⌈·⌉` quote, `⌊·⌋` stage, `↓` interpret.
* **Safety:** Tower Rule, no `𝒰_i:𝒰_i`, carriers only for down.
* **Barriers:** `anti` quotes; values by default; `unquote` optional extension.
* **Aboutness:** `|·|` lowest viable level; `≈̇` role‑preserving iso.

### 20.2 Roadmap

* Extend with **modalities per level** (`□_ℓ, ◇_ℓ`).
* Add **parametricity**: an abstraction theorem across levels (relational interpretation in a fibration).
* Develop **erotetic completeness** at object level and a **reflection principle** for meta‑questions.
* Integrate **autopoietic fixed points** guarded by levels for safe self‑regeneration.

---

*End of §2: Typed Kinds & Stratified Universes (20pp v0.1).*


---

# MetaPrincipia Autopoiētica — Part I §3

## Formation, Binding, Evaluation Contexts (Twenty‑Page Slab, v0.1)

> **Aim.** Specify the formation rules, binding discipline, and evaluation contexts for 𝒞\_A, including call‑by‑meaning small‑step semantics, evaluation under torsion, and the **regen** operator as a *context transformer* `regen: Γ → Γ′`.

**Conventions.** Syntactic equality `≡`. Definitional equality `≡₍def₎`. Propositional equality `=`. Level tags `@ℓ` (from §2). Aboutness footprint `|t|`; equivalence `≈̇`. Torsion sites marked `τ⋔`.

**Map (20 pages).**

1. Overview & Interfaces
2. Raw Syntax (Abstract Grammar)
3. Formation Rules I (Atoms, Predication, Relators)
4. Formation Rules II (Meta‑relators, Selectors, Regen)
5. Binding & Substitution
6. Free/Bound Occurrences; α‑Conversion
7. Evaluation Contexts (Call‑by‑Meaning)
8. Principal Redexes & Barriers
9. Torsion Contexts & Coherence
10. Small‑Step Rules (Core)
11. Small‑Step with Torsion
12. Regen as Γ→Γ′ Transformer
13. Preservation & Progress (Sketches)
14. Normalization & Confluence (ℛ\_A excerpt)
15. Aboutness Stability under Evaluation
16. Worked Examples I (Formation→Evaluation)
17. Worked Examples II (Torsion & Barriers)
18. Worked Examples III (Regen Pipelines)
19. BNF Deltas, Tables, and Laws
20. Test Harness Spec & Checklists

---

## Page 1 — Overview & Interfaces

We refine §1–§2 with operational detail:

* **Formation** yields well‑typed terms.
* **Binding** controls variable capture and scoping across strata.
* **Evaluation** proceeds **call‑by‑meaning**: reduce the *meaning‑bearing head* subject to declared barriers.
* **Torsion** changes attachment sites and evaluation order in controlled ways.
* **Regen** is a first‑class *contextual* operator: `regen: Γ → Γ′`, updating the judgmental environment.

Interfaces:

* Proof‑theoretic: sequent rules respect scoping.
* Denotational: `⟦·⟧` projects to truth conditions; aboutness `|·|` is invariant under neutral rewrites.
* Categorical: torsion and regen map to functors and algebra/coalgebra structure.

---

## Page 2 — Raw Syntax (Abstract Grammar)

Let `Var` be a countable set. Abstract forms:

```
Term t,u ::= x | c | P(t) | R(t,u) | λx:τ. t | t u |
             meta-of(R) | para-through(R,S) | trans(R) | anti(R) |
             Sel(t) | regen(t) | seed(t) | fold(t) | unfold(t) |
             let x = t in u | match t with … |
             (t ∧ u) | (t ∨ u) | (t → u) | ¬t | □t | ◇t
Role r  ::= Agent | Theme | …
Type τ  ::= Thing | Prop | Role | Rel | MetaRel | Question | Regen | τ→τ | τ×τ | …
Sel     ::= who | what | which | where | when | why | how
R,S     ::= base relator identifiers (in, on, …) or compound relators
```

Meta‑level forms inherit this grammar with `@ℓ` tags.

---

## Page 3 — Formation Rules I (Atoms, Predication, Relators)

**Atoms.**

```
(Atom-Intro)     a ∈ 𝔸                 ⇒   Γ ⊢ a : Thing
(Pred-Intro)     P : Thing→Prop, Γ ⊢ a:Thing  ⇒   Γ ⊢ P(a) : Prop
```

**Relators.** Binary by default; higher arity via currying or labeled roles.

```
(Rel-Intro)      Γ ⊢ R:Thing×Thing→Prop, Γ ⊢ x:Thing, Γ ⊢ y:Thing ⇒ Γ ⊢ R(x,y):Prop
(Role-Rel)       Γ ⊢ t:Theme, Γ ⊢ s:Surface                       ⇒ Γ ⊢ on(t,s):Prop
```

**Logic.** Standard intro/elim for `∧, ∨, →, ¬`; modalities per model.

---

## Page 4 — Formation Rules II (Meta‑relators, Selectors, Regen)

**Meta‑relators.**

```
(Meta-Intro)     Γ ⊢ R:Rel               ⇒ Γ ⊢ meta-of(R) : Rel
(Para-Intro)     Γ ⊢ R:Rel, Γ ⊢ S:Rel    ⇒ Γ ⊢ para-through(R,S) : Rel
(Trans-Intro)    Γ ⊢ R:Rel               ⇒ Γ ⊢ trans(R) : Rel
(Anti-Intro)     Γ ⊢ R:Rel               ⇒ Γ ⊢ anti(R) : Rel
```

**Selectors.**

```
(Q-Intro)        Γ ⊢ φ:Prop              ⇒ Γ ⊢ Sel(φ) : Question
```

**Regen.** (Context‑transforming operator.)

```
(Regen-Term)     Γ ⊢ x:Thing             ⇒ Γ ⊢ regen(x):Thing
(Seed-Term)      Γ ⊢ x:Thing             ⇒ Γ ⊢ seed(x):Regen
(Fold/Unfold)    Γ ⊢ t:τ                 ⇒ Γ ⊢ fold(t):τ,  Γ ⊢ unfold(t):τ
```

A judgmental form for contexts will refine how `regen` acts on `Γ` (Page 12).

---

## Page 5 — Binding & Substitution

**Binding forms.** `λx:τ. t`, `∀x:τ. φ`, `∃x:τ. φ`, `let x=t in u`, pattern binders in `match`.

**Free variables `FV(t)`** and **bound variables `BV(t)`** defined inductively.
**Capture‑avoiding substitution** `t[x:=u]` standard; extended across relators and meta‑relators trivially (they do not bind).

**Side condition.** Substitution across `anti(R)` is structural (as data); no evaluation inside unless unquoted.

---

## Page 6 — Free/Bound Occurrences; α‑Conversion

* α‑renaming preserves binding structure.
* α‑equivalence extends to questions and regen forms.
* Aboutness `|t|` factors α‑renaming out; labels use role/predicate identities, not variable names.

---

## Page 7 — Evaluation Contexts (Call‑by‑Meaning)

**Strategy.** *Call‑by‑meaning* = reduce the innermost principal redex along the semantic spine, left‑to‑right, unless blocked by a barrier or torsion directive.

**Evaluation contexts.**

```
E ::= [·] | P(E) | R(E,t) | R(t,E) | (E ∧ t) | (t ∧ E) | (E ∨ t) | (t ∨ E)
    | (E → t) | (t → E) | ¬E | □E | ◇E | Sel(E)
    | metaσ(E) | para-through(E,S) | para-through(R,E) | trans(E) | anti(E)
    | regen(E) | seed(E) | fold(E) | unfold(E) | let x=E in t | match E with …
```

`σ` ranges over meta heads. Parentheses control evaluation order.

**Head position.** For application `t u`, reduce `t` to a head value before reducing `u`.

---

## Page 8 — Principal Redexes & Barriers

**Principal redexes.**

* β: `(λx:τ. t) u`.
* Meta‑hoist: `meta-of(R)(a,R′)` (when `a,R′` are values).
* Para‑assoc: `(para-through(R,S)) ∘ T`.
* Trans‑functor: `trans(R ∘ S)`.
* Logical principals: `¬¬φ`, distributive rewrites (if declared).
* Regen β‑like: `fold(unfold(t))`, `unfold(fold(t))`.

**Barriers.**

* `anti(R)(args)` is a *quoted* value. No interior reduction until an explicit `unquote` (extension) or rewrite that moves the barrier.

---

## Page 9 — Torsion Contexts & Coherence

A **torsion context** is a pair `(E, T)` where `T` is a *warp profile* assigning precedence and attachment changes to occurrences of meta‑operators.

**Torsion markers.** Annotate a subterm by `τ⋔` to indicate pending scope warp. Example: `τ⋔ meta-of(in)(x,R′)`.

**Coherence laws (schematic).**

1. **Commutation:** if `meta` and `trans` commute on `R`, then `meta(trans(R)) ≡ trans(meta(R))` and evaluation orders yield a common normal form.
2. **Associator for para‑through:** right‑associate chains to canonical form.
3. **Monotone slot fusion:** `meta(R)(x, y∧φ) ≡ meta(R)(x,y) ∧ φ` when slot‑2 monotone.

**Policy.** A torsion profile may *delay* or *advance* a meta rewrite; the policy must be confluent with coherence.

---

## Page 10 — Small‑Step Rules (Core)

We write `t ↦ u` for one step in the absence of torsion directives; `t ↦_T u` when obeying a torsion profile.

**β.** `(λx:τ. t) v ↦ t[x:=v]` if `v` is a value.
**Rel‑arg.** `x ↦ x′ ⇒ R(x,y) ↦ R(x′,y)`; `y ↦ y′ ⇒ R(v,y) ↦ R(v,y′)`.

**Meta‑hoist.** `meta-of(R)(a, R′) ↦ Lift(R)(a, RelObj(R′))`.

**Para‑assoc.** `(para-through(R,S)) ∘ T ↦ para-through(R, S ∘ T)`.

**Trans‑functorial.** `trans(R ∘ S) ↦ trans(R) ∘ trans(S)`.

**Fold/Unfold.** `fold(unfold(t)) ↦ t`, `unfold(fold(t)) ↦ t`.

**Barriers.** No step into `anti⟨·⟩`.

---

## Page 11 — Small‑Step with Torsion

With profile `T`, priorities can change:

* If `T` prefers meta first: `meta` rewrites fire before logical or relator rewrites at the same spine depth.
* If `T` is barrier‑biased: moves *around* `anti` rather than through it.

**Determinism under profile.** For a fixed `T`, head‑reduction is deterministic up to α.

**Confluence.** Provided coherence laws and oriented rules, different torsion profiles converge to the same canonical normal form.

---

## Page 12 — Regen as Γ→Γ′ Transformer

**Judgmental contexts.**

```
Γ ::= · | Γ, x:τ | Γ, φ | Γ, ann(k, v)
```

Annotations `ann(k,v)` hold meta‑information (timestamps, authority, regen lineage).

**Regen operator on contexts.**

* `regen` updates context by adding a fresh *successor binding* and lineage links.

**Rule (contextual).**

```
(Regen-Γ)   Γ ⊢ x:Thing
            ————————————————————————————————  (fresh x′)
            regen: Γ ↦ Γ′ = Γ, x′:Thing, ann(lineage, x↦x′)
```

The *term* `regen(x)` denotes the produced successor **and** triggers the context update.

**Subject reduction for contexts.** If `Γ ⊢ t:τ` and `regen: Γ↦Γ′`, then `Γ′ ⊢ t:τ` (old bindings persist). Additionally, `Γ′ ⊢ regen(x):Thing` and lineage predicates become available.

**Idempotence up to iso.** `regen(regen(x)) ≡₍iso₎ regen(x)`; lineage composes.

---

## Page 13 — Preservation & Progress (Sketches)

**Preservation.** If `Γ ⊢ t:τ` and `t ↦ u`, then `Γ ⊢ u:τ`. Proof by cases on rules; meta‑hoist preserves type via `Lift` typing; para/trans by relator typing; fold/unfold by (co)algebra laws.

**Progress.** If `⊢ t:τ` closed, then `t` is a value or there exists `u` with `t ↦ u`. Barrier cases classify as values; torsion profiles fix rule priority.

**Contextual preservation.** If `regen: Γ↦Γ′`, any prior typing remains valid in `Γ′`.

---

## Page 14 — Normalization & Confluence (ℛ\_A excerpt)

**Termination measure.** `(meta‑height, constructor depth, redex weight, regen‑nest)`. Barriers freeze interior redexes; they are counted as values.
**Local confluence.** Critical pairs: (β vs meta‑hoist), (para‑assoc vs trans), (fold/unfold vs meta‑hoist). Joinability ensured by coherence.

**Newman.** Terminating + local confluence ⇒ confluence on normalizing fragment.

---

## Page 15 — Aboutness Stability under Evaluation

**Claim.** If `t ↦ u` via a neutral rewrite, then `|t| ≅ |u|`.
**Neutral rewrites.** β, η (when admitted), associators, functorial lifts, fold/unfold, and torsion reorders that do not add/remove anchors.
**Regen effect.** `regen(x)` *adds* a regen‑edge from `x` to `x′` in `|·|`; stability holds for parts not involving the new edge.

---

## Page 16 — Worked Examples I (Formation→Evaluation)

**E1. Basic formation.**

```
Γ ⊢ Cat:Thing, Γ ⊢ Mat:Thing, Γ ⊢ on:Thing×Thing→Prop
Γ ⊢ on(Cat,Mat):Prop
```

**Evaluation.** Already in canonical relator form; value.

**E2. Predicate + relator.** `Sit(Cat) ∧ on(Cat,Mat)` reduces by simplifying `Sit(Cat)` if `Sit` is defined; no interaction with `on`.

---

## Page 17 — Worked Examples II (Torsion & Barriers)

**E3. Torsion order.**

```
T: prefer meta before logic
why( in(Cat,Box) ∧ on(Cat,Mat) )
```

Under `T`, analyze `in` and `on` choice first if encapsulated via `meta‑why` lifting; otherwise standard `why` scopes over the conjunction.

**E4. Barrier.**

```
anti(on)(Cat,Mat)
```

Value; no reduction under `anti`. `unquote` would expose inner form (extension, not core).

---

## Page 18 — Worked Examples III (Regen Pipelines)

**E5. Single regen.**

```
Γ ⊢ A:Thing
regen(A)  ⟹  Γ′ = Γ, A′:Thing, ann(lineage, A↦A′)
```

Term result denotes `A′`. Context gains `A′` and lineage.

**E6. Regen + bind.**

```
bind(regen(A))
```

Binds `A′` into the active scene; aboutness acquires `A —regen→ A′` and scene‑attachment edge.

**E7. Regen idempotence (iso).** `regen(regen(A)) ≈ iso(regen(A))` with composed lineage.

---

## Page 19 — BNF Deltas, Tables, and Laws

**BNF delta.**

```
EContext ::= ... | Torsion '[' E ']' | Barrier '[' t ']'
Torsion  ::= 'meta-first' | 'logic-first' | 'rel-first' | policy-id
```

**Operator laws (selected).**

* `para-through` right‑associative canonicalization.
* `trans` strong monoidal: `trans(R⊗S) ≡ trans(R)⊗trans(S)`.
* `regen` idempotent up to iso; monotone w\.r.t. context extension.

**Typing table snippets.**

| Rule    | Premises      | Conclusion                        |
| ------- | ------------- | --------------------------------- |
| Regen‑Γ | `Γ ⊢ x:Thing` | `regen: Γ↦Γ′`, `Γ′ ⊢ x′:Thing`    |
| Barrier | `Γ ⊢ R:Rel`   | `Γ ⊢ anti(R)(args):Prop` is value |

---

## Page 20 — Test Harness Spec & Checklists

**Harness.**

* Parser with torsion profiles and barriers.
* Typechecker verifying context transforms for regen.
* Rewriter implementing ℛ\_A and torsion scheduling.
* Aboutness engine computing `|t|` and diff under steps.
* KG adapter to record lineage annotations.

**Property tests.**

1. **Preservation:** types are stable under `↦`.
2. **Progress:** closed well‑typed terms step or are values.
3. **Confluence:** different torsion profiles yield same canonical form.
4. **Regen:** `Γ↦Γ′` monotone; old derivations remain valid.
5. **Aboutness:** stability under neutral rewrites; explicit regen edges recorded.

---

*End of §3: Formation, Binding, Evaluation Contexts (20pp v0.1).*



---
PATCH HOTFIX

Agreed. Here are corrected foundations.

## 1) Termination of ℛ\_A

### 1.1 Fix the measure

Use a **defect vector** `Δ(t) ∈ ℕ^6`, ordered lexicographically:

1. `m_meta(t)`: # of **non-hoisted** `meta-of` occurrences (i.e., heads that still await their hoist rule).
2. `m_para(t)`: # of **left inversions** in `para-through` trees.

   * Compute on the binary tree with `para` as the node label: `m_para = Σ nodes (left_weight)`, where `left_weight(node) = 1` iff the left child is itself a `para` node. This counts precisely the number of needed right-associations.
3. `m_trans(t)`: # of unfactored `trans(R∘S)` patterns.
4. `m_beta(t)`: # of β-redexes.
5. `m_fold(t)`: # of `fold(unfold(·))` and `unfold(fold(·))` pairs.
6. `m_barrier(t)`: 0 if no **illegal** step attempts under `anti`; otherwise 1 (barriers remain values, so this stays 0 in legal reductions).

`Δ` is well-founded since `ℕ^6` with lex order is well-founded.

### 1.2 Each rule strictly decreases `Δ`

* **Meta-hoist** `meta-of(R)(a,R′) ↦ Lift(R)(a,RelObj(R′))`:
  decreases `m_meta` by 1. Other components unchanged.
* **Para-assoc** `(para(R,S))∘T ↦ para(R, S∘T)`:
  decreases **exactly** one left inversion at the root, hence `m_para − 1`. (Constructor depth may grow, but is irrelevant since only `m_para` measures associativity defects.)
* **Trans-factor** `trans(R∘S) ↦ trans(R)∘trans(S)`:
  decreases `m_trans` by 1.
* **β**: decreases `m_beta` by 1 (creation of new redexes is handled by lex order: `m_beta` sits after meta/para/trans).
* **Fold/Unfold**: each contraction decreases `m_fold` by 1.
* **Barriers**: no rule enters `anti⟨·⟩`; `m_barrier` stays 0.

Therefore every legal step strictly decreases `Δ`. Termination follows.

---

## 2) Tower rule hole and self-totalization

### 2.1 Precise stratification of reification

* Reified relations into `B` at level `ℓ`: `RelObj_ℓ(B) : 𝒰_{i+1}` and **code only level-`ℓ` relations**.
* **Formation**: `Γ ⊢_ℓ R:A→B→Prop ⟹ Γ ⊢_{ℓ+1} δ(R):RelObj_ℓ(B)`.
* **Quantification** over `RelObj_ℓ(B)` is **only** at level `ℓ+1`.

### 2.2 No self-totalization schema

Add a side condition to comprehension:

> (**Predicativity**) There is **no** term `T@ℓ` whose denotation depends on a quantifier over the **entire** `RelObj_ℓ(B)` unless `T` is **at** `ℓ+1`.

Formally: if `φ` contains `∀R′:RelObj_ℓ(B). …` then `φ : Prop@ℓ+1`. Hence you cannot internalize “totality of level-ℓ reified objects” **at** `ℓ`. Any use at `ℓ` requires `↓` with a carrier and proof obligation; we forbid a carrier that reifies that **total** quantification (no `↓ : Code(∀RelObj_ℓ(·)) → …`). This blocks the Russell-style diagonal.

---

## 3) Aboutness equivalence `≈̇` (non-circular)

### 3.1 Typed hypergraphs

A **typed role-hypergraph** is `H = (V,E,inc,τ,σ)`:

* `V`: vertices.
* `E`: hyperedges.
* `inc: E → List(V)` with **fixed arity and role positions**; write `inc(e)[i] = v`.
* `τ: V → Types` (vertex types).
* `σ: E → Sig`, where each signature `s ∈ Sig` is a tuple `(label, roles, polarity, meta_flag)` with:

  * `label ∈ {in,on,through,…,meta-of,para-through,…}`
  * `roles = ⟨ρ₁,…,ρ_k⟩`, each `ρ_i ∈ {Agent,Theme,…}`.
  * `polarity ∈ {→, ←, bidir}` when relevant.
  * `meta_flag ∈ {0,1}` marking reification edges.

### 3.2 Role-preserving isomorphism

An isomorphism `(f:V→V′, g:E→E′)` satisfies, for all `e∈E` and positions `i`:

1. **Incidence preservation**: `inc′(g(e))[i] = f( inc(e)[i] )`.
2. **Type preservation**: `τ′( f(v) ) = τ(v)`.
3. **Signature preservation**: `σ′( g(e) ) = σ(e)` (same label, roles, polarity, meta\_flag).

Define `|t|` as the hypergraph produced by compositional translation of `t`. Then:

* `≈̇` is **equality up to** role-preserving isomorphism as above.
* Reflexive/symmetric/transitive are immediate since we require graph isomorphism.
* **Congruence**: if contexts compose edges by signature-compatible gluing, the homomorphisms compose; hence `C[t₁,u₁]≈̇C[t₂,u₂]` when `t₁≈̇t₂` and `u₁≈̇u₂`.

No circularity: “role-preserving” is a check against `σ`.

---

## 4) Categorical semantics (statements with proofs)

### 4.1 Scene category

Objects: types with roles (e.g., `Theme(Thing)`, `Location(Thing)`), write `A,B,…`.

Morphisms: **binary relations** `R ⊆ A×B` satisfying the relator’s typing/constraints.

* **Identity** on `A`: `Id_A = { (a,a) | a∈A }`. Typing holds by construction.
* **Composition**: `(S ∘ R) = { (a,c) | ∃b. (a,b)∈R ∧ (b,c)∈S }`.
* **Associativity**: relational composition is associative; proof is standard set-theoretic equivalence.
* **Left/right unit**: `Id` is the neutral element under relational composition.

Thus **Scene** is a category.

### 4.2 `para-through`

By definition `⟦para-through(R,S)⟧ = S∘R`. The associativity/unit laws in the calculus mirror the category laws above; the rewrite to right-assoc is a choice of **canonical bracketing**, not a semantic claim.

### 4.3 Endofunctors (minimal guarantees)

Define on objects the identity. On morphisms:

* `F_meta(R:A→B) := R_meta : A→RelObj(B)` with `R_meta(a, r̂) :≡ (a,b)∈ι(r̂)` for some `b`.

  * **Preserves identities**: `F_meta(Id_A) = Id_A` (no change of domain; codomain is reified but identity still relates `a` to the code of `(a,a)`; if such codes are not admitted, restrict claim to endofunctor on the **relator subcategory**, not identities between base objects—this addresses the edge case).
  * **Preserves composition**: `F_meta(S∘R) = F_meta(S) ∘ F_meta(R)` since both define existence of matching witnesses via reified codomains.
* `F_trans`: a structure map sending each relator to its oriented dual; identities preserved; composition preserved when orientation is functorial (assumed only for the declared class).

**Adjunctions**: only claim **conditionally**. If `ι: RelObj(B)→𝒫(A×B)` is full and faithful and there exists `U` forgetting reification with unit/counit satisfying triangle equalities, then `Reify ⊣ U`. Absent these side conditions, we **do not assert** an adjunction.

---

## 5) Autopoietic semantics Π (computational content)

### 5.1 Configurations and state

Use a small-step abstract machine.

* **Config**: `(σ, t)` where `σ = ⟨N, L, K⟩` with:

  * `N`: fresh-name supply.
  * `L`: lineage map `Thing → list(Thing)` (parents/children).
  * `K`: knowledge base of asserted facts.
* **Result**: `(σ′, v)` with `v` a value.

### 5.2 Rules for `regen`

* **Alloc**

  ```
  (σ, regen(x)) ↦ (σ[x′:=fresh(N), L:=L∪{x↦x′}], x′)
  ```

  where `x′` is fresh; record lineage edge `(x,x′)` in `L` and optionally `K`.

* **Bind (optional op)**

  ```
  (σ, bind(regen(x))) ↦ (σ’, unit)
  ```

  with `σ’` updating `K` to assert scene attachment of `x′`.

* **Idempotence up to iso**
  Operationally: repeated `regen` is permitted but each step records a new descendant; the **equational theory** may quotient multiple successive `regen` into a canonical representative for denotational purposes.

* **Laws**

  * Monotonicity: `K ⊆ K′` after regen/bind.
  * No-duplication: `x′` fresh ensures distinctness.
  * Aboutness: add a regen edge in `|·|` from `x` to `x′`.

This is **not** a generic state step: `regen` is the **only** constructor allowed to mint fresh objects and to enforce lineage invariants. That is its computational content.

---

## 6) Paraconsistent isolation `Prop_⋈` and collapse

Choose an LFI-style core (Logic of Formal Inconsistency).

### 6.1 Two judgments

* Classical zone: `Γ ⊢ φ`.
* Paraconsistent zone: `Γ ⊢⋈ φ`.

### 6.2 LP-style base (truth-functional sketch)

Use designated values `{T, B}` (true, both) vs `{F}`. Explosion is **not** valid in `⊢⋈`.

Sequent rules (excerpt):

* **Introduction** rules mirror classical for `∧,∨,→`, but EFQ (`φ,¬φ ⊢ ψ`) is **absent** in `⊢⋈`.
* **Transport**: from `Γ ⊢ φ` infer `Γ ⊢⋈ φ`. Not conversely.

### 6.3 Consistency operator `◦`

Add unary `◦φ` meaning “φ is consistent”.

Rules:

* If `Γ ⊢⋈ φ` and `Γ ⊢⋈ ¬φ` and `Γ ⊢ ◦φ`, then **collapse** to classical: `Γ ⊢ φ` **or** `Γ ⊢ ¬φ` according to policy (see below).
* From `Γ ⊢ φ` derive `Γ ⊢⋈ φ` and `Γ ⊢ ◦φ`.

### 6.4 Collapse policies (make them explicit)

* **Authority**: a labeled fact `auth(e, φ)` licenses `◦φ` and selects `φ` over `¬φ`.
* **Recency**: a timestamp order picks one side; yields `◦φ` by rule.
* **Minimal-change**: prefer the side that preserves more theorems in `K`.

Formally, add meta-inference:

```
(Policy)   Γ ⊢⋈ φ, Γ ⊢⋈ ¬φ,  Policy(Γ,φ) ⇒ Γ ⊢ ◦φ  and  Γ ⊢ choice(φ) 
```

where `choice(φ) ∈ {φ, ¬φ}` determined by the policy. Only then can explosion be simulated in the classical zone; otherwise contradictions stay **isolated** in `⊢⋈`.

---

## 7) Clean statements to replace hand-waving

* **Termination**: proved via `Δ`.
* **Tower safety**: predicativity + level-indexed reification + no `↓` for totalities.
* **Aboutness**: `≈̇` = isomorphism of typed role-hypergraphs `(V,E,inc,τ,σ)`.
* **Scene is a category**: identities and associativity hold by relational semantics; `para` = composition; canonical bracketing is a normalization choice.
* **Endofunctors**: specify laws per class; drop unconditional adjunction claims.
* **Autopoiesis**: concrete SOS rules for `regen`; invariants and aboutness effect specified.
* **Paraconsistency**: LFI core with `◦` and explicit collapse policies.


---



# MetaPrincipia Autopoiētica — Part I §4

## Relators & Self‑Descriptive Operators (Twenty‑Page Slab, v0.1)

> **Thesis.** Meaningful scenes are assembled by **relators**—typed, role‑aware morphisms that endow semantic structure with topology. **Meta‑relators** act functorially on relators and scenes, enabling self‑description, controlled scope warps, and safe reflection in the autopoietic calculus **𝒞\_A**.

**Standing notation.** Syntactic equality `≡`. Definitional equality `≡₍def₎`. Aboutness equivalence `≈̇`. Levels `@ℓ` per §2. Torsion marker `τ⋔`. Reified carriers `RelObj, RoleObj, FrameObj`. Paraconsistent zone `Prop_⋈`. Calculus: 𝒞\_A.

**Page plan (20).**

1. Overview & Roles
2. Relators as Role‑Structured Morphisms
3. Typing & Arity Schemas
4. Topological Semantics of Core Relators
5. Scene Category and Monoidal Product
6. Relator Composition & Para‑Through
7. Self‑Descriptive Layer: Reification & `meta‑of`
8. Meta‑Relators as Endofunctors
9. Strong/Op‑Lax Variants & Coherence
10. Barrier/Quotation Operator `anti`
11. Transforms `trans` and Orientation
12. Self‑Descriptive Operators (S‑Ops)
13. Evaluation Under Torsion
14. Soundness & Normalization Excerpts
15. Aboutness Invariants for Relators
16. Erotetic Interfaces: Questions about Relations
17. Worked Examples I (Topologies)
18. Worked Examples II (Self‑Description)
19. BNF, Laws, and Tables
20. Test Harness Spec & Checklists

---

## Page 1 — Overview & Roles

Relators are the **semantic glue**. Each relator `R` is a typed arrow between role‑refined object classes. The canonical minimal roles:
`Agent, Theme, Experiencer, Instrument, Source, Goal, Path, Location, Time, Manner, Cause, Surface`.

A **role‑structured scene** is a typed diagram whose edges are relator instances. The calculus enforces arity, role compatibility, and coherence conditions between simultaneous relators on the same anchors.

---

## Page 2 — Relators as Role‑Structured Morphisms

### 2.1 Type and signature

Base form (binary):

```
R : (ρ₁: A) × (ρ₂: B) → Prop
```

where `ρᵢ` are role tags and `A,B` are object types (often `Thing`).

### 2.2 Role predicates and constraints

Each relator declares **slot constraints**, e.g. for `on`:

```
Surface(B)  (B must admit surface contact)
Contactable(A) (A must admit support/contact)
```

Constraints appear as side conditions in typing or as premises in sequent rules.

### 2.3 Variance and polarity

Slots may be **monotone**, **antitone**, or **non‑monotone** for meta‑distribution. Example: `in(Theme, Location)` is monotone in the second slot under set inclusion models of `Location`.

---

## Page 3 — Typing & Arity Schemas

### 3.1 Binary default; higher arity

Higher‑arity relators are curried or packaged as hyper‑edges via `FrameObj` (e.g., `between(x,y;z)`):

```
between : (Theme1:Thing)×(Theme2:Thing)×(Reference:Thing) → Prop
```

### 3.2 Labeled roles in typing

```
Γ ⊢ t:Theme, Γ ⊢ s:Surface ⇒ Γ ⊢ on(t,s) : Prop
Γ ⊢ x:Theme1, Γ ⊢ y:Theme2, Γ ⊢ z:Reference ⇒ Γ ⊢ between(x,y;z) : Prop
```

### 3.3 Co‑typing and compatibility

Two relators may impose a commuting constraint. For instance `in(x,B)` and `on(x,B)` commute if `B` is a container with interior surface; otherwise a tension `⋈` is recorded.

---

## Page 4 — Topological Semantics of Core Relators

We assign **topological intuitions** consistent with categorical semantics:

* `in(x,y)`: inclusion/containment. Semantics as `x ∈ interior(y)` or a containment relation `C ⊆ D` in a locale/poset view.
* `on(x,y)`: contact/support. Requires `Surface(y)`. Induces a contact relation `Contact(x,y)` obeying reflexive constraints on surfaces.
* `through(x,y)`: path traversal. Semantics via existence of a path `π` with trace inside `y`.
* `across(x,y)`: path with *crossing property*; requires boundary traversal.
* `between(x,y;z)`: betweenness. Ternary relation with axioms of Pasch‑type or metric convexity.
* `over/under(x,y)`: oriented height relation; partial order enriched with orientation.
* `near(x,y)`: proximity; uniform space or metric with threshold predicate.
* `about(x,y)`: topic linkage; an aboutness edge in the hypergraph layer.

These choices fix **coherence** and **composition** behavior for `para‑through` (§6).

---

## Page 5 — Scene Category and Monoidal Product (Revised)

### Scene as a Category (with proofs)

* **Objects** `A,B,…`: role‑refined types (e.g., `Theme(Thing)`, `Location(Thing)`).
* **Morphisms** `R ⊆ A×B`: typed binary relations meeting slot constraints of the relator.

**Identity.** `Id_A = {(a,a) | a∈A}` is typed `A→A`. For any `R ⊆ A×B`,
`Id_B∘R = {(a,c) | ∃b. (a,b)∈R ∧ (b,c)∈Id_B} = {(a,c) | (a,c)∈R} = R`, and similarly `R∘Id_A = R`.

**Composition.** `(S∘R)(a,c) :≡ ∃b. R(a,b) ∧ S(b,c)`. This is associative by standard set‑theoretic reasoning:
`T∘(S∘R) = {(a,d) | ∃c. (∃b. R(a,b)∧S(b,c)) ∧ T(c,d)} = {(a,d) | ∃b. R(a,b) ∧ (∃c. S(b,c)∧T(c,d))} = (T∘S)∘R`.

Hence **Scene** is a category. In 𝒞\_A, `para‑through` **denotes** composition; the right‑association rewrite fixes a canonical bracketing.

### Monoidal product

## Tensor `⊗` on objects is role‑product; on morphisms it is pointwise. Symmetry swaps role factors. Coherence follows from Set; we do not assume extra structure beyond declared role products.

## Page 6 — Relator Composition & Para‑Through

**Definition.**

```
para‑through : Rel×Rel → Rel
⟦para‑through(R,S)⟧(x,z) ≡ ∃y. ⟦R(x,y)⟧ ∧ ⟦S(y,z)⟧
```

**Laws.**

* Associativity (up to declared associator): `para‑through(R, para‑through(S,T)) ≡ para‑through(para‑through(R,S), T)`.
* Identity: `para‑through(Id, R) ≡ R ≡ para‑through(R, Id)`.
* Right‑associative **canonicalization** under normalization.

These laws induce the Scene composition.

---

## Page 7 — Self‑Descriptive Layer: Reification & `meta‑of` (Revised)

Reify relations into carriers:

* `RelObj(B)` with interpretation `ι: RelObj(B) → 𝒫(A×B)`.

**Lift.**
`⟦meta‑of(R)⟧ : A×RelObj(B)→{0,1}` with
`⟦meta‑of(R)(a, r̂)⟧ ≡ holds(r̂,a) ≡ ∃b. (a,b)∈ι(r̂)`.

**Typing.** If `Γ ⊢ R: A→B→Prop`, `Γ ⊢ a:A`, `Γ ⊢ r̂: RelObj(B)`, then `Γ ⊢ meta‑of(R)(a, r̂): Prop`.

## This is a precise clause, not prose; it fixes the semantics used by the proof rules.

## Page 8 — Meta‑Relators as Endofunctors

Meta‑relators `M` act on **RelCat\_A** (the subcategory of relators and rewrites):

* Objects: relators as morphisms.
* Morphisms: relator rewrites/equalities.
* `M: RelCat_A → RelCat_A` is an (op‑)lax endofunctor with structure maps preserving or controlling composition.

**Examples.**

* `meta`: reifies targets; arrow `A→B` becomes `A→RelObj(B)`.
* `trans`: orientation transform; e.g., `over ↦ under` under reflection morphism.
* `anti`: comonadic quotation; blocks interior computation.

Natural transformations encode coherence between different meta‑paths.

---

## Page 9 — Strong/Op‑Lax Variants & Coherence

A meta‑relator `M` is **strong monoidal** if there is a natural isomorphism `μ: M(R) ∘ M(S) ⇒ M(R∘S)` and `M(Id) ≅ Id`. It is **op‑lax** if we only have a morphism one way.

**Coherence axioms (schematic).**

1. **Associativity:** pentagon for `para‑through`.
2. **Unit:** triangle for `Id`.
3. **Meta/Para interchange:** if `M` is strong, `M(para‑through(R,S)) ≅ para‑through(M(R), M(S))`.

These supply the commuting diagrams used in normalization.

---

## Page 10 — Barrier/Quotation Operator `anti`

`anti` quotes a relator application as data.

**Typing.** `Γ ⊢ R:Rel ⇒ Γ ⊢ anti(R) : Rel`.

**Operational.** `anti(R)(args)` is a **value**; interior evaluation blocked. Optional `unquote` removes the barrier in an extended system. Categorical reading: CoKleisli of a comonad `Q` representing quotation; maps into a reflective subcategory of *frozen* scenes.

**Use.** Prevent premature distribution or preserve as object of discussion.

---

## Page 11 — Transforms `trans` and Orientation

`trans` lifts geometric orientation or dualizes slots.

**Examples.**

* `trans(over) ≡ under`, `trans(under) ≡ over`.
* For path relators: `trans(through)` might reverse traversal (opposite category of paths).

`trans` may be strong monoidal for parallel composition and op‑lax for sequential composition (path reversal is order‑reversing).

---

## Page 12 — Self‑Descriptive Operators (S‑Ops)

We define a family of *self‑descriptive operators* that internalize meta‑talk as ordinary terms while respecting levels.

### 12.1 Descriptor δ

```
δ : Rel → RelObj
δ(R)  ≡  code of R with its slot constraints and declared laws
```

`δ(R)` is a carrier; `↓δ(R)` is not admissible unless a policy admits *unfolding* codes.

### 12.2 Choice χ

`χ` asks for **which** relation satisfies a property at a site:

```
χ_R(a) : RelObj   with  holds(χ_R(a), a)
```

Operationally, `χ_R` may be a nondeterministic or choice operator returning a relation object consistent with context.

### 12.3 Preference π

`π` selects a relation from an equivalence class under aboutness `≈̇`, favoring a declared metric (e.g., minimal torsion).

### 12.4 Self‑application guard σ

A typed guard preventing same‑level self‑application by forcing a lift:

```
σ(R) :≡ meta-of(R)   (forces talk‑about rather than use‑as)
```

**S‑Ops Law.** `meta-of(R)(a, χ_R(a))` reduces to `⊤` when `χ_R` is sound and `holds(χ_R(a),a)` witnessed.

---

## Page 13 — Evaluation Under Torsion

A torsion profile `T` prioritizes rewrites among `meta`, `para`, `trans`, logic, and S‑Ops.

**Policies.**

* **meta‑first:** evaluate lifts and S‑Ops before applying relators.
* **rel‑first:** execute relators, defer self‑description.
* **barrier‑biased:** prefer to propagate barriers; avoid unfreezing.

**Confluence.** Coherence guarantees that different `T` yield the same canonical scene modulo isomorphism.

---

## Page 14 — Soundness & Normalization (Revised)

### Termination via a Defect Vector

Use `Δ(t) = (m_meta, m_para, m_trans, m_beta, m_fold, m_barrier) ∈ ℕ^6` lex‑ordered.

* `m_meta`: count of non‑hoisted `meta-of` heads.
* `m_para`: count of left inversions in the `para` tree (nodes with a `para` left child).
* `m_trans`: count of unfactored `trans(R∘S)`.
* `m_beta`: count of β‑redexes.
* `m_fold`: count of `fold(unfold(·))`/`unfold(fold(·))` pairs.
* `m_barrier`: 0; barriers are values and never stepped.

Each rule strictly decreases one component: hoist ↓`m_meta`, assoc ↓`m_para`, factor ↓`m_trans`, β ↓`m_beta`, fold/unfold ↓`m_fold`. Thus ℛ\_A terminates.

### Local Confluence

Critical pairs `(β ⊔ meta)`, `(para‑assoc ⊔ trans‑factor)`, `(fold/unfold ⊔ meta)` are joinable by the declared coherence diagrams. By Newman, **confluence** holds on normalizing terms.

### Soundness excerpt

## `para‑through` is interpreted as relational composition; `meta‑of` as reified satisfaction. The sequent rules in §4 and §7 are sound under these clauses.

## Page 15 — Aboutness Invariants for Relators (Revised)

### Typed role‑hypergraphs

`H = (V,E,inc,τ,σ)` with `V` vertices, `E` hyperedges; `inc: E→List(V)`; `τ:V→Types`; `σ:E→(label,roles,polarity,meta_flag)`.

### Role‑preserving isomorphism

Isomorphism `(f,g)` satisfies `inc′(g(e))[i]=f(inc(e)[i])`, `τ′(f(v))=τ(v)`, and `σ′(g(e))=σ(e)` for all edges `e` and positions `i`.

## Construct `|t|` compositionally. Define `t₁≈̇t₂` iff `|t₁|` and `|t₂|` are isomorphic in this sense. Then `≈̇` is an equivalence relation and a **congruence** under 𝒞\_A composition. Neutral rewrites (assoc/functorial lifts/fold‑unfold) preserve `|·|`; `meta‑of` adds a meta‑edge to `RelObj`; `anti` tags quarantine without altering anchors.

## Page 16 — Erotetic Interfaces: Questions about Relations

Questions that range over relations use reification:

```
which( meta-of(on)(x, R′) ∧ Surface(y) )
```

This asks: *which* reified relation `R′` relates `x` to some `y` with a surface property.

Answerhood relation `Ans` checks `holds(R′,x)` and any side constraints. Meta‑questions keep level `@1` unless carriers are interpreted down.

---

## Page 17 — Worked Examples I (Topologies)

**E1. Containment vs. contact.**

* `in(Cat,Box)` and `on(Cat,Box)` may coexist only if `Box` has an interior surface accessible to `Cat`. Otherwise record `⋈`.

**E2. Traversal.**

* `through(Needle,Cloth)` entails existence of a path. `across` additionally requires a boundary crossing. Composition with `in` respects path inclusion.

**E3. Betweenness.**

* `between(A,B;C)` is symmetric in `A,B` and respects convexity constraints: if `between(A,B;C)` and `between(B,D;C)` then `between(A,D;C)` under geodesic convexity.

---

## Page 18 — Worked Examples II (Self‑Description)

**E4. Relation choice.**

```
χ_on(Cat) → R′ ;  meta-of(on)(Cat, R′)
```

Choosing a reified relation object that holds of `Cat` yields a true `meta‑of` statement.

**E5. Why this relator?**

```
why( meta-of(in)(x, R′) )
```

Asks for reasons that the **in** relation was chosen or holds, rather than e.g. `on`.

**E6. Barrier use.**

```
anti(through)(x,y)
```

Freezes traversal statements for meta‑analysis without performing composition with neighboring relators.

---

## Page 19 — BNF, Laws, and Tables

**BNF delta (relators & S‑Ops).**

```
Rel       ::= BaseRel | MetaRel '(' Rel {',' Rel} ')' | SOp '(' Rel {',' Arg} ')'
BaseRel   ::= 'in' | 'on' | 'at' | 'by' | 'with' | 'from' | 'to' | 'through' | 'over' | 'under' | 'between' | 'across' | 'near' | 'about'
MetaRel   ::= 'meta-of' | 'para-through' | 'anti' | 'trans'
SOp       ::= 'δ' | 'χ' | 'π' | 'σ'
```

**Typing snippets.**

* `meta‑of(R): Rel`, `para‑through(R,S): Rel`, `anti(R): Rel`, `trans(R): Rel`.
* `δ: Rel→RelObj`, `χ_R: A→RelObj(B)` for each `R: A→B→Prop`.

**Key laws.**

* `para` assoc/unit; `trans` distributes when declared; `anti` is idempotent quotation; `meta` hoist; S‑Ops soundness (`holds(χ_R(a),a)`).

---

## Page 20 — Test Harness Spec & Checklists

**Parser.** Supports role annotations, meta‑relators, S‑Ops, barriers.

**Typechecker.** Enforces role constraints, variance, and carrier usage.

**Rewriter.** Implements canonicalization (`para` assoc), hoisting (`meta`), orientation transforms (`trans`), barriers (`anti`).

**Aboutness engine.** Builds hypergraphs; computes `≈̇`; records meta‑edges for reified relations.

**Erotetic engine.** Checks answerhood for relation questions.

**Property tests.**

1. `para` associativity up to canonicalization.
2. `meta` soundness vs. `RelObj` interpretation.
3. `anti` blocks interior steps.
4. `trans` invertibility for declared pairs (e.g., `over/under`).
5. Aboutness invariance under neutral rewrites.

---

*End of §4: Relators & Self‑Descriptive Operators (20pp v0.1).*



