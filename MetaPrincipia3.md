# MetaPrincipia Autopoiētica — Part III: Applications & Executable Interpretants

## §9. Natural Language as Autopoietic Scene Assembly — Prepositions as Topological Operators; Interrogatives as Selectors over Aboutness (Twenty‑Page Slab, v0.1)

> **Thesis.** Natural‑language meaning can be compiled into **scene assemblies**: typed role‑hypergraphs composed by **relators** (prepositions and thematic heads) and queried by **interrogatives** as *aboutness selectors*. Grammar is a front‑end to the calculus 𝒞\_A; this section specifies the mapping, proves invariants, and gives executable pipelines and evaluations.

**Prereqs.** Part I (symbols, kinds), Part II §5–§8 (aboutness, recursive axioms, barriers, regen monad).

**Page plan (20):**

1. Goal & scope
2. Linguistic interface: inventories
3. Syntax → Scene typing
4. Prepositions as topological operators
5. Adpositions & case systems
6. Relator composition and coercions
7. Interrogatives as selectors
8. Question semantics over aboutness
9. Ambiguity: scope, attachment, and torsion
10. Noun phrases as anchor constructors
11. Verbs as relator schemata
12. Clausal operators: negation, modality, aspect
13. Cross‑lingual mapping
14. Execution pipeline
15. Worked examples I
16. Worked examples II
17. Evaluation metrics
18. Error modes & guards
19. Test harness
20. Next steps

---

## Page 1 — Goal & scope

We operationalize a front‑end from surface strings to scene assemblies `(⟦·⟧_E, ⟦·⟧_I, |·|)` with: (i) prepositions/adpositions as **topological relators** (attachment sites + orientation + constraints), (ii) interrogatives as **selectors** over the aboutness layer, (iii) a normalization regime that preserves `≈̇` while resolving local syntactic choices.

---

## Page 2 — Linguistic interface: inventories

**Relators (English core).** `in, on, at, to, from, into, onto, out_of, over, under, through, across, between, among, with, without, for, by, about, of, before, after, during, within, beyond, along, against, near`.

**Roles.** `Agent, Theme, Experiencer, Instrument, Source, Goal, Path, Location, Time, Manner, Cause, Surface, Possessor`.

**Interrogatives.** `who, what, which, where, when, why, how, how_many, how_much`.

Each item carries a **signature**: arity, role schema, selectional constraints (e.g., `on(Theme, Surface)` with predicate `Surface(y)`), and **topology** (containment, contact, adjacency, path).

---

## Page 3 — Syntax → Scene typing

We define a typed interface `Γ ⊢ s : Scene` via a CCG/UD‑compatible mapping.

**Anchors.** NPs map to anchors: `⟦NP⟧ : Thing` with features (number, animacy) used in role constraints.

**Relator phrases.** PP/ADP heads map to relators: `⟦P⟧ : (Role₁:Thing)×(Role₂:Thing)→Prop` or higher‑arity for `between/among`.

**Composition.** Head directionality yields application order; aboutness is insensitive to head‑final vs head‑initial choice (torsion dictionary `D*`).

**BNF.**

```
Scene   ::= Clause | Scene Conj Scene
Clause  ::= NP VP | VP
VP      ::= V NP | V PP* NP? | V NP PP*
PP      ::= P NP | P CoordNP
CoordNP ::= NP ('and' NP)+
QClause ::= Wh Clause | Wh Aux NP VP
```

---

## Page 4 — Prepositions as topological operators

Each `P` is a **topological map** with parameters:

```
σ(P) = (label=P, roles=⟨ρ1,ρ2⟩, topo, constraints)
```

`topo ∈ {containment, contact, adjacency, path, orientation}`.

**Examples.**

* `in(Theme, Container)` → containment; nests.
* `on(Theme, Surface)` → contact; requires `Surface(y)`.
* `through(Theme, Conduit)` → path; composes with `across`.

**Axioms (selected).**

* `through ∘ across` associative; **alignment law** resolves orientation.
* `in` distributes over nested containers under non‑overlap.

---

## Page 5 — Adpositions & case systems

Non‑prepositional languages use **cases** as relators. Map dative to `to/for` (Goal/Benefactive), instrumental to `with(Instrument,Theme)` or `by(Agent,Passive)`. Postpositions map identically but with head‑final torsion. Case stacking (`ablative‑dative`) yields `para‑through( from , to )`.

---

## Page 6 — Relator composition and coercions

**Relator schemas.** Verbs expose slots typed by roles; prepositions **coerce** or refine them.

Example: `give : Agent×Theme×Goal → Event`. `to NP` fills `Goal`; `from NP` fills `Source`.

**Coercion rule.** If a verb slot `ρ` lacks a PP, a default relator fills it (e.g., `Goal=implicit hearer`). These defaults are policy‑controlled and flagged in aboutness.

**Para‑composition.** PP chains map to composed relators via `para‑through`; aboutness collects edges; ANF canonicalizes.

---

## Page 7 — Interrogatives as selectors

Selectors `Wh` are **queries over aboutness**:

```
who   : Prop → Question over Agent/Experiencer anchors
what  : Prop → Question over Theme/Artifact anchors
where : Prop → Question over Location/Path/Surface anchors
when  : Prop → Question over Time anchors
why   : Prop → Question over Cause/Motive edges
how   : Prop → Question over Manner/Instrument/topology
which : (Set, Prop) → Question constrained by set
```

`Wh` does **not** alter aboutness; it projects a retrieval over `|·|`.

---

## Page 8 — Question semantics over aboutness

Given a scene `φ` with ANF hypergraph `H=|φ|`:

* `where(φ)` returns anchors of role types in `{Location, Surface, Path}` incident to edges of interest.
* `who(φ)` returns `Agent/Experiencer` anchors.
* `why(φ)` inspects `Cause/Motive` edges; if absent, returns **affordance** tasks (cf. §8) to collect evidence.

**Formal.** Let `R_Wh` be the role filter; answer set:

```
Ans_Wh(φ) = { v ∈ V(H) | τ(v) ∈ R_Wh ∧ ∃e∈E(H). v∈inc(e) ∧ σ(e)∈Scope(Wh) }
```

---

## Page 9 — Ambiguity: scope, attachment, and torsion

Attachment ambiguity (`with the telescope`) is handled by **candidate scenes** with identical aboutness backbones but different local attachments.

* **Pack** alternatives in a *zone set* `Z={H₁,H₂,…}` with weights.
* Maintain **torsion** equivalences: `over/across` alignment; `on/atop` synonyms.
* **Selectors** compute answers under *credal aggregation* or *policy selection*; explicit collapse (§7) can choose one.

**Invariant.** All candidates agree on a shared aboutness *core*; selectors on that core are stable.

---

## Page 10 — Noun phrases as anchor constructors

`NP` is an **anchor constructor**:

* **Proper nouns** → unique anchor id.
* **Definites** → resolve via `T=R∘U` canonicalization (salience, recency).
* **Indefinites** → spawn fresh anchor via `regen` with low weight.

**Modifiers.** Adjectives map to unary predicates attached to anchors; intersective ones do not alter relator edges. Relational nouns (`edge of graph`) introduce relators (`of`/genitive) with `Possessor` or structural roles.

---

## Page 11 — Verbs as relator schemata

Lexical verb entries define **frames** with required roles; PPs bind or refine them.

Example entries:

```
sit: Theme×Surface → Event
put: Agent×Theme×Goal → Event   // PP[to NP] supplies Goal
move: Theme×Path → Event         // PP[through/along] supplies Path
```

**Aspect** marks event structure but does not change aboutness edges; it annotates weights/timestamps.

---

## Page 12 — Clausal operators: negation, modality, aspect

* **Negation** `¬φ` keeps `|φ|` unchanged; extensional truth flips; aboutness unaffected.
* **Modality** `□,◇` reindex intensional layer; aboutness stable (RA‑7).
* **Aspect** (prog/perf) affects time stamps and event granularity; aboutness role set fixed.

**Questions under operators.** `where(¬φ)` = `where(φ)`; `where(□φ)` = `where(φ)`.

---

## Page 13 — Cross‑lingual mapping

Map case/PP systems to relator signatures with a **torsion dictionary** per language. Examples:

* Japanese `ni` (dative/locative) → `{to, at}` with role disambiguation by verb class.
* Russian `v/na` (in/on) with case switches; surface/contact constraint distinguishes.
* Hindi postpositions `mẽ/par/tak/se` → `{in/on/up_to/from}`.

**Guarantee.** Aboutness maps are **language‑invariant** up to torsion; cross‑lingual paraphrases share `≈̇`.

---

## Page 14 — Execution pipeline

**Stages.**

1. **Parse** (any syntactic formalism that yields heads/deps).
2. **Anchor construction** for NPs with `regen` and coreference policy.
3. **Relator extraction** from PPs, particles, cases.
4. **Scene assembly** into hypergraph `H`.
5. **ANF canonicalization** and torsion normalization `D*`.
6. **Question answering** via role‑filtered graph queries.
7. **Regen monad** `T` for canonicalization and gap generation.

**Complexities.** Linear in tokens; ANF `O(|E| log |E|)`; QA near‑linear in incident edges.

---

## Page 15 — Worked examples I

**E1.** “The cat sits on the mat.”

```
Anchors: cat, mat
Relator: on(Theme=cat, Surface=mat)
Scene: edge(on; cat→mat), pred(sit(cat))
where(…)= {mat}; who(…)= {cat}
```

**E2.** “Alice put the book on the table.”

```
Frame: put(Agent=Alice, Theme=book, Goal=table)
Relator: on(book, table) coerced to Goal
where(…)= {table}; what(…)= {book}; who(…)= {Alice}
```

---

## Page 16 — Worked examples II (attachment & ambiguity)

**E3.** “I saw the man with a telescope.”

```
Two scenes: Instrument vs NP‑modifier
S₁: see(Experiencer=I, Theme=man); with(Instrument=telescope)
S₂: see(Experiencer=I, Theme=man_with(telescope))
Core aboutness: {I —see→ man}
who(…)= {I}; what(…)= {man}; how(…)= {telescope} in S₁ only
```

**E4.** “We walked across the field into the forest.”

```
Relators: across(field) ∘ into(forest) on Path
Para‑composition canonicalizes; where= {field, forest}; path recorded
```

---

## Page 17 — Evaluation metrics

* **Aboutness preservation** vs human paraphrase: WL‑kernel on ANF; report `AUC` distinguishing paraphrase vs non‑paraphrase.
* **Selector accuracy** on QA datasets (who/where/when); use graph answers.
* **Attachment robustness**: agreement on core aboutness across alternatives.
* **Cross‑lingual invariance**: `≈̇` rate across aligned corpora.

---

## Page 18 — Error modes & guards

* **Polysemy of prepositions** (`by` agent vs proximity). Guard with verb frames and role predictors.
* **Coercion overreach**: avoid forcing `on` to Goal where semantics demands Location.
* **Coref failures**: wrong anchor merging. Use `regen` with decay until evidence accumulates.
* **Parsing noise**: keep aboutness stable by ignoring purely syntactic alternations.

---

## Page 19 — Test harness

Property tests:

* Torsion invariance under `D*` (e.g., `on/atop`).
* Para‑associativity on `through/across/into`.
* Selector stability under negation/modality.
* Cross‑lingual `≈̇` on aligned pairs.
* Regen idempotence under repeats.

Benchmarks: intrinsic (QA, parsing) and extrinsic (retrieval, KB alignment).

---

## Page 20 — Next steps

1. Release a reference front‑end: UD parser → 𝒞\_A scene assembler → ANF canonicalizer → selector engine.
2. Build cross‑lingual torsion dictionaries; evaluate invariance.
3. Integrate §8’s constructive incompleteness to surface questions where aboutness lacks evidence (e.g., `why`).

---

*End of Part III §9: Natural Language as Autopoietic Scene Assembly (20pp v0.1).*


---


# MetaPrincipia Autopoiētica — Part III: Applications & Executable Interpretants

## §10. Mathematics from Meaning — Numbers as Role‑Anchored Abstractions; Category Theory as Reflective Scene Logic (Twenty‑Page Slab, v0.1)

> **Thesis.** Mathematical objects arise inside 𝒞\_A as **role‑anchored abstractions** over scenes: numbers from counting and ordering roles, functions from relator coherence, and algebraic laws from scene composition. Category theory is the **reflective logic of scenes**: it captures identity, composition, limits, and recursion for aboutness‑preserving transformations. This section defines numbers, arithmetic, and categorical structure internal to 𝒞\_A and proves core soundness and induction principles.

**Prereqs.** Part I (symbols, kinds, roles), Part II §5–§8 (aboutness, recursive axioms, barriers, regen monad), Part III §9 (scene assembly).

**Page map (20):**

1. Roadmap & stance
2. Scenes, roles, and abstraction
3. Cardinality from Theme‑incidence
4. Ordinality from Path/Order roles
5. Arithmetic as scene algebra
6. Peano object (NNO) in `Hyp`
7. Recursion & induction internal to scenes
8. Rational, real, measure via roles
9. Sets, functions, relations as scene morphisms
10. Category of scenes `Scene` and `Hyp`
11. Yoneda meaning principle
12. Limits, colimits, products, coproducts
13. Monoidal and closed structure
14. Adjunctions from question/answer
15. Paraconsistent numerics (⋈ counts)
16. Algorithms: counting & ordering from language
17. Worked examples I (cardinal/ordinal)
18. Worked examples II (arithmetic word problems)
19. Test harness & formal guarantees
20. Next steps & export schema

---

## Page 1 — Roadmap & stance

Mathematics is *internalized* as invariants of aboutness. Numbers quantify **how many Themes** attach under a role/relator; ordinals quantify **in what order** along Path or Location sequences; arithmetic composes scenes. Category theory then abstracts these constructions across all scenes.

Design constraints:

* Role‑sensitivity: counts depend on role filters.
* Torsion‑invariance: synonyms do not change numbers.
* Zone‑locality: contradictions do not explode counts across zones.
* Regen‑stability: canonicalization does not change numbers except by explicit creation/deletion.

---

## Page 2 — Scenes, roles, and abstraction

Take a scene hypergraph `H=(V,E,inc,τ,σ)` (§5). Fix a **role filter** `ρ` (e.g., `Theme`, `Agent`, `Surface`) and a **relator signature** `Σ` (e.g., `on`, `in`, `edge_of`). Define the **ρ‑frontier**:

```
Frontier_ρ^Σ(H) := { v∈V | ∃e∈E. σ(e)∈Σ ∧ v occurs in inc(e) at role ρ }
```

Numbers will be invariants of `Frontier_ρ^Σ(H)` modulo a chosen equality (identity, coref, torsion collapse).

**Equality policy.** An equivalence relation `≈` on anchors (e.g., coreference, synonym merge). Counts are taken on `V/≈`.

---

## Page 3 — Cardinality from Theme‑incidence

**Definition (ρ‑cardinality).** For `H` and role filter `ρ` with relators `Σ`, the **cardinality** is

```
#_{ρ,Σ}(H) := |Frontier_ρ^Σ(H) / ≈|
```

Special case: `#_Theme^{on}(H)` = number of Themes *on something*. More general: restrict by a second role value (e.g., `on(Theme=*, Surface=table)`).

**Functoriality.** If `f : H → H′` is a role‑preserving isomorphism (or torsion action) then `#_{ρ,Σ}(H)=#_{ρ,Σ}(H′)`.

**Hume’s Principle (scene form).** Two collections have the same number iff a bijection exists between their role frontiers:

```
#_{ρ,Σ}(H)=#_{ρ,Σ}(H′)  ⇔  ∃ bijection  b: Frontier_ρ^Σ(H)/≈  ≅ Frontier_ρ^Σ(H′)/≈
```

This **defines** finite cardinals internally to `Hyp`.

---

## Page 4 — Ordinality from Path/Order roles

Fix a **linear order relator** `≺` realized as a Path or Time sequence. Given a chain `v₀ ≺ v₁ ≺ ⋯ ≺ v_{n−1}` in `H`, define the **order type** of the chain as the unique `n∈ℕ` up to order‑isomorphism.

**Definition (ordinal along ρ).** The ordinal of `Frontier_ρ^Σ(H)` under order relator `≺` is the order‑type of the induced subgraph restricted to ρ‑anchors, when such a linearization exists by policy (ties broken or zones split).

**Successor and limit.** Successor adds a fresh terminal via `regen`; limits are colimits of ω‑chains in `Hyp` with embeddings preserving `≺`.

---

## Page 5 — Arithmetic as scene algebra

Let `A,B` be two ρ‑frontiers, assumed disjoint modulo `≈`.

* **Addition**: `|A ⊕ B| := |A| + |B|` via **disjoint union of anchors** (tensor `⊗` on independent subscenes).
* **Multiplication**: `|A ⊗_role B| := |A|·|B|` via **role product**: pair each `a∈A` with `b∈B` through a product relator `pair(a,b)`.
* **Exponentiation**: `|B^A| := |Hom_scene(A,B)|` where morphisms encode total role‑respecting maps; in finite cases this matches `|B|^{|A|}`.

**Theorem (Finite arithmetic soundness).** Under disjointness and independence assumptions enforced by barriers, the above operations satisfy commutativity and associativity up to scene isomorphism, with distributivity witnessed by canonical wiring of relators.

---

## Page 6 — Peano object (NNO) in `Hyp`

We define a **Natural Numbers Object** `(N, zero, succ)` internal to `Hyp`.

* `N` is a scene template whose anchors are `{0,1,2,…}` realized as a chain via a `succ` relator with roles `Prev,Next` and a distinguished `0`.
* `zero : 1 → N` picks the anchor `0` (a one‑vertex scene into `N`).
* `succ : N → N` adds the `Next` edge.

**Universal property.** For any object `(X, x0, f)` with `x0:1→X` and `f:X→X`, there exists a unique `u:N→X` such that:

```
u∘zero = x0
u∘succ = f∘u
```

`u` is **primitive recursion**. Existence is by fold over the chain; uniqueness by zone‑wise induction.

---

## Page 7 — Recursion & induction internal to scenes

**Induction schema (scene form).** For predicate `P` over anchors of `N`:

```
P(0) ∧ ∀n (P(n) → P(succ n))  ⇒  ∀n P(n)
```

`P` lives as a subscene classifier; proof is a morphism into a truth object `Ω` inside `Hyp`.

**Primitive recursion on scenes.** Given `g:1→X` and `h:X→X`, define `fold_N(g,h): N → X` by `fold_N(0)=g`, `fold_N(succ n)=h(fold_N(n))`. This implements iteration constructs over scenes (counts, aggregations, enumerations).

---

## Page 8 — Rational, real, measure via roles

**Naturals → Integers.** Quotient pairs `(m,n)` under `≈` where `(m,n) ~ (m+k,n+k)`; represent as difference of ρ‑frontiers in disjoint zones.

**Rationals.** Pairs `(m,n>0)` with multiplicative equivalence `(m,n) ~ (m·k,n·k)`; realized as counts on product scenes with barriers ensuring positivity of denominators.

**Reals (sketch).** Cauchy sequences of rationals internal to `Hyp` using **aboutness metrics** (WL kernel or path metrics) as norm; reals are equivalence classes of Cauchy scenes. Alternatively use Dedekind cuts as zone‑closed predicates over rationals.

**Measure.** A role‑measure `μ_ρ` assigns non‑negative values to sets of ρ‑anchors with σ‑additivity across disjoint zones; integrals are limits of simple functions realized as weighted scene sums.

---

## Page 9 — Sets, functions, relations as scene morphisms

We take **objects** to be typed anchor collections with role predicates; **morphisms** are **role‑respecting maps** realized by relator edges of type `map : A×B → Prop` with **functional** and **total** constraints:

```
∀a∈A ∃! b∈B. map(a,b)
```

Relations are arbitrary subscenes of `A×B`. Composition is relator chaining with uniqueness preservation.

**Exponentials.** `B^A` exists when functional relators can be packaged as anchors representing functions, with evaluation `ev : B^A × A → B` a relator satisfying the universal property; holds for finite scenes and under mild finiteness conditions in `Hyp`.

---

## Page 10 — Category of scenes `Scene` and `Hyp`

* **`Scene`**: objects are finite typed anchor sets with role/relator edges; morphisms are role‑preserving graph homomorphisms that respect signatures.
* **`Hyp`**: category of all typed aboutness hypergraphs (possibly infinite) with role‑preserving homomorphisms.

Both have identities (identity homomorphism) and associative composition.

**Adhesivity.** `Hyp` is adhesive: pushouts along monos exist and are stable; enables double‑pushout rewriting (ℛ\_A) and safe gluing of scenes.

---

## Page 11 — Yoneda meaning principle

For any anchor/object `A` in `Scene`, its **meaning profile** is the presheaf

```
Ŝ(A) := Hom_Scene(–, A)
```

assigning to every context `X` the set of **ways A can be seen inside X**. By **Yoneda**, natural transformations from Ŝ(A) to any presheaf `F` correspond to elements of `F(A)`. Intuitively: *to know A is to know its role in all scenes*.

**Consequences.**

* Two anchors with isomorphic Ŝ profiles are indistinguishable by aboutness‑preserving queries.
* Numbers can be represented as presheaves counting ρ‑incidences; arithmetic becomes presheaf algebra.

---

## Page 12 — Limits, colimits, products, coproducts

In `Hyp` and finite `Scene`:

* **Products**: pullback of projections over shared anchors; corresponds to intersection of aboutness constraints.
* **Coproducts**: disjoint unions of scenes.
* **Equalizers/Co‑equalizers**: enforce or quotient role equations (coreference resolution, synonym collapse).
* **Pullbacks** model substitution and role filling; **pushouts** glue along shared subscenes.

These categorical limits/colimits realize set‑like and algebraic constructions for mathematics internal to scenes.

---

## Page 13 — Monoidal and closed structure

`(Scene, ⊗, I)` with tensor `⊗` = **independent parallel composition**; unit `I` = empty scene. Symmetric monoidal via swap relabeling.

**Closedness (partial).** For finite scenes with functional relators we form **internal hom** `B ⊸ A` as scene of functional maps; evaluation and currying witness monoidal closed structure on a subcategory of scenes (cartesian closed in purely functional fragment).

**Enrichment.** Enrich `Scene` in a cost/weight quantale `(Q, ⊕, ⊗)` to track confidence or measure; composition cost is multiplicative, coproduct cost is additive.

---

## Page 14 — Adjunctions from question/answer

Selectors `Wh` and **answer assemblers** form Galois connections. For a fixed role filter `R_Wh` and scene `X`:

```
Ask_X : Hyp → Set,   Ans_X : Set → Hyp
Ask_X ⊣ Ans_X   with   Ask_X(H) ⊆ S  ⇔  H ≤ Ans_X(S)
```

Adjunction encodes **optimal answers**: `Ans_X` freely generates a scene satisfying a set of answers; `Ask_X` extracts answers from a scene. This aligns with §9 interrogatives.

---

## Page 15 — Paraconsistent numerics (⋈ counts)

If contradictory facts produce `⋈` on edges, define **credal counts**:

```
#^-_{ρ,Σ}(H) = lower count using only ◦‑validated anchors
#^+_{ρ,Σ}(H) = upper count including all anchors, ignoring ⋈
```

Return intervals `[ #^- , #^+ ]`. Collapse policies (§7) refine to a point. Arithmetic lifts to intervals with **Kleene algebra** style bounds.

**Conservation.** In absence of collapse, addition/multiplication are sub/super‑additive w\.r.t. interval endpoints.

---

## Page 16 — Algorithms: counting & ordering from language

Given a sentence or document:

1. Build scene `H` (§9).
2. Choose `ρ, Σ` from the query.
3. Coref policy → compute quotient `V/≈`.
4. Count `Frontier_ρ^Σ(H)` and compute orders via detected `≺` (temporal, enumerative markers).
5. If ambiguity/⋈ present, produce intervals and zone‑conditioned alternatives.

Complexity: linear in edges; coref adds learned cost; orders from dependency/semantic cues.

---

## Page 17 — Worked examples I (cardinal/ordinal)

**Example A (cardinal).** “Three apples on the table.”

```
H: anchors a1,a2,a3, t; edges on(ai,t)
#_{Theme,on}(H)=3
```

**Example B (ordinal).** “The second runner finished before the third.”

```
Order ≺ from rank; ordinals 2 and 3 realized as positions in Path/Time. succ relates positions.
```

**Example C (mixture).** “Two books on each shelf.”

```
Parametric counting: for each shelf s, #_{Theme,on|Surface=s}(H)=2; total = 2·#shelves
```

---

## Page 18 — Worked examples II (arithmetic word problems)

**Baskets.** “Alice has 2 apples. Bob gives her 3 apples. How many now?”

```
Scene 1: have(Alice, {a,a}); Scene 2: give(Bob, {b,b,b}, Alice)
Addition via disjoint union under possessive role → 5
```

**Rectangles.** “How many squares on a 3×4 grid?”

```
Counts via product roles: positions = 3·4; squares computed by sum_{k=1}^{min(3,4)} (3−k+1)(4−k+1)
Encodable as fold over N with multiplication
```

**Exponentials.** “In how many ways can 3 keys map to 2 boxes?” → `2^3 = 8` using internal hom size.

---

## Page 19 — Test harness & formal guarantees

**Properties.**

* Role‑invariance: `#_{ρ,Σ}` respects isomorphisms and torsion.
* Addition/multiplication laws hold under independence assumptions.
* NNO universal property verified by property tests (fold/induction).
* Interval counts refine monotonically under collapse policies.

**Proof sketches.**

* Hume’s Principle in `Hyp` via existence of bijections as isomorphisms of frontiers.
* NNO uniqueness up to isomorphism using standard categorical argument internalized to `Hyp`.

---

## Page 20 — Next steps & export schema

**Next steps.**

1. Implement `#_{ρ,Σ}` and order extraction with zone awareness; expose APIs.
2. Provide internal `N` object and `fold_N` library for arithmetic on scenes.
3. Add interval arithmetic for `⋈` counts; integrate policy hooks.

**Export schema extension (JSON).**

```json
{
  "Counts": [{
    "scene_id": "…",
    "role": "Theme",
    "relators": ["on"],
    "filter": {"Surface": "table"},
    "lower": 2,
    "upper": 2,
    "policy": "strict"
  }],
  "Orders": [{
    "scene_id": "…",
    "order_relator": "before",
    "chain": ["runner#1","runner#2","runner#3"],
    "ordinals": {"runner#2": 2, "runner#3": 3}
  }]
}
```

---

*End of Part III §10: Mathematics from Meaning (20pp v0.1).*


---

# MetaPrincipia Autopoiētica — Part III: Applications & Executable Interpretants

## §11. Reflexive Systems & Semantic Paradox — Y‑Combinators, Fixed‑Point Meaning, and Torsion Handling in Self‑Modeling Agents (Twenty‑Page Slab, v0.1)

> **Thesis.** Reflexivity is inevitable in autopoietic semantics. We give **fixed‑point meaning** constructions compatible with the tower rule, a **guarded Y** for computation, and **torsion handling** for agents that model themselves. Paradox is isolated by barriers (§7) and turned into **productive tension** via the regen monad (§8).

**Standing context.** 𝒞\_A syntax/typing (Part I), tri‑layer semantics (Part II §6), barrier calculus & paraconsistency (Part II §7), regen monad (Part II §8).

**Page map (20):**

1. Motivation and design aims
2. Domains and orders for meaning
3. Monotone/continuous operators
4. Tarski–Knaster fixed points (extensional)
5. Guardedness and the delay modality ▷
6. The guarded Y‑combinator `Y▸`
7. Operational semantics of `Y▸`
8. Denotational adequacy and soundness
9. Diagonalization with carriers (safe self‑reference)
10. Truth, quotation, and the stratified `Tr@ℓ`
11. The Liar under barriers: existence, isolation, policies
12. Torsion in self‑models: meta‑of, anti, trans
13. Agents with reflective state; belief fixed points
14. Decision fixed points and value alignment hooks
15. Collapse risks and meltdown detectors
16. Algorithms for reflexive evaluation
17. Worked examples I (recursive definitions)
18. Worked examples II (self‑modeling agents)
19. Test harness and verifiable guarantees
20. Next‑step plan and export schema

---

## Page 1 — Motivation and design aims

Reflexive systems must:

* Admit **fixed‑points** for meaning and behavior.
* Avoid **meta‑level collapse** (Part I tower rule).
* Localize paradox via **barriers** and **zones** (§7).
* Make contradiction a **constructive affordance** (§8).
  We combine domain‑theoretic semantics with our tri‑layer `S(t)=(⟦t⟧_E,⟦t⟧_I,|t|)`.

---

## Page 2 — Domains and orders for meaning

Let `Val_E` be extensional values with a **complete partial order** (CPO) `(V_E, ⊑_E)` where `⊥` is undefined/least info.
Similarly `(V_I, ⊑_I)` pointwise over worlds; `(H, ⊑_A)` for hypergraphs ordered by **information inclusion**: `H⊑_A H′` iff `V(H)⊆V(H′)` and every edge in `H` occurs in `H′` with equal or weaker flags.

**Product CPO.** `V = V_E × V_I × H` with order product. Directed lubs exist componentwise.

---

## Page 3 — Monotone/continuous operators

A **meaning transformer** `F : V→V` is **monotone** if `x⊑y ⇒ F(x)⊑F(y)` and **Scott‑continuous** if it preserves lubs of directed sets. Constructors of 𝒞\_A induce such `F` (under guards for intensional/world indices and zone‑wise ANF for `H`).

**Lemma (Constructor continuity).** For each constructor `C`, the induced `F_C` is continuous on `V` when barriers are respected and regen state is fixed.

---

## Page 4 — Tarski–Knaster fixed points (extensional)

For monotone `F` on a CPO with `⊥`, the **least fixed point** is `lfp(F)=⊔_{n≥0} F^n(⊥)`. We interpret recursive specifications `X = F(X)` extensionally as `lfp(F)` when `F` is monotone/continuous.

**Axiom (Layered Tarski).** On `V`: if `F` is continuous componentwise then `lfp(F)` exists; projections are the lfps of projected operators.

---

## Page 5 — Guardedness and the delay modality ▷

We introduce a **delay** type `▷τ` and a term former `next : τ→▷τ`. Only `unbox : ▷τ→τ` is allowed **behind a barrier**:

```
Γ ⊢ t:τ ⇒ Γ ⊢ next t : ▷τ
Γ ⊢ u:▷τ,   in_zone Z ⇒ Γ ⊢ unbox u : τ  (Z‑guard)
```

Recursive definitions must be **guarded** by `next` under at least one constructor (relator, modality, or barrier). This ensures **contractivity** in a metric semantics or continuity in the CPO with a step‑index.

---

## Page 6 — The guarded Y‑combinator `Y▸`

Define `Y▸ : (▷τ→τ) → τ` by:

```
Y▸ F  ≔  let rec x = F (next x) in x
```

Typing rule:

```
Γ ⊢ F : ▷τ→τ  ⇒  Γ ⊢ Y▸ F : τ
```

`next` enforces a delay; evaluation uses **k‑unfolds** via step index.

**Equation.** `Y▸ F  ≅  F (next (Y▸ F))` (β‑like up to next/unbox laws).

---

## Page 7 — Operational semantics of `Y▸`

Small‑step with step index `k∈ℕ`:

```
⟨k, Y▸ F⟩  ↦  ⟨k, let x = F (next x) in x⟩
⟨k, let x = v in x⟩ ↦ ⟨k, v⟩
⟨k, F (next x)⟩  ↦  ⟨k−1, F (next x)⟩   if k>0
```

Evaluation halts when `k=0` (value up to one unfold). Under increasing `k` we approximate the limit; **productivity** holds because each unfold consumes one unit of guardedness.

---

## Page 8 — Denotational adequacy and soundness

**Theorem (Adequacy).** If operationally `Y▸ F` `k`‑unfolds to value approximants `v_k`, then `⟦v_k⟧` forms an ω‑chain whose lub is `lfp(⟦F⟧)`. Conversely, the denotational lfp is approximated by the operational semantics.

**Corollary.** `Y▸` implements least fixed points compatible with barriers/zones and tri‑layer projections.

---

## Page 9 — Diagonalization with carriers (safe self‑reference)

**Quotation.** `quote_ℓ : Prop@ℓ → PropObj@ℓ+1`. **Evaluation.** `eval_ℓ : PropObj@ℓ+1 → Prop@ℓ` only behind trusted barrier and via `↓`.

**Diagonal schema (safe).** For `P@ℓ` with kind `PropObj@ℓ → Prop@ℓ` define at `ℓ+1`:

```
Diag(P) ≔ P (quote_ℓ(P))   // lives at ℓ+1
```

`Diag(P)` cannot collapse levels because it talks *about* `P` via a carrier; truth about `Diag(P)` uses `Tr@ℓ+1`.

---

## Page 10 — Truth, quotation, and the stratified `Tr@ℓ`

Define partial truth predicates `Tr@ℓ : Prop@ℓ → Prop@ℓ+1` with T‑schema only for object‑level formulas:

```
Tr@ℓ(φ) ↔ φ   (as a statement at level ℓ+1 about φ@ℓ)
```

No global `Tr` over all levels exists. Reflection `↓` is permitted for closed `φ@ℓ` through a certified evaluation channel; logs record the use of `↓`.

---

## Page 11 — The Liar under barriers: existence, isolation, policies

Construct `L@ℓ+1`:

```
L  ≔  ¬Tr@ℓ( eval_ℓ(quote_ℓ(L_↓)) )
```

where `L_↓` is a **frozen** copy of `L` only usable behind `anti⟨·⟩`. Two outcomes:

1. If `eval_ℓ` is disabled, `L` is **ungrounded**; remains opaque within its zone.
2. If enabled, `L` yields `⋈` within `Z_L`. Policies (§7) can **collapse** or keep paraconsistent. Cross‑zone explosion is impossible (Local Non‑Explosion).

---

## Page 12 — Torsion in self‑models: meta‑of, anti, trans

Self‑models use `meta‑of` to treat relations as objects. **Torsion** denotes representation choices:

* `trans(R)` toggles orientation (e.g., input/output role swap) in the model.
* `anti⟨M⟩` keeps a model **non‑executing**, safe for analysis.
* `para‑through(R,S)` composes modelled relations; restricted to the same zone.

**Coherence Law.** Modelling an operation then executing equals executing then modelling, up to barrier annotations: `meta‑of(exec(C))(M) ≈ meta‑exec(meta‑of(C)(M))` when `C` is pure.

---

## Page 13 — Agents with reflective state; belief fixed points

Agent state: `Σ = ⟨Env, Bel, Des, Pol⟩` (environment, beliefs, desires, policy). A **self‑model** `M : Σ → ModelObj` is part of `Bel`.

Belief update as operator `F_Bel : Bel → Bel` consuming observations and `M`.

**Belief fixed point.** Seek `Bel* = F_Bel(Bel*)`. If `F_Bel` is monotone in a CPO of **belief lattices** (sets of scenes ordered by inclusion with `⋈` annotations), `lfp(F_Bel)` exists; `Y▸` computes approximations.

**Introspection.** A query `q` into `M` produces predicted beliefs about its own future belief. Guard it with `next` to avoid immediate self‑collapse.

---

## Page 14 — Decision fixed points and value alignment hooks

Define **decision operator** `F_Act : (Obs → Dist(Act)) → (Obs → Dist(Act))` that maps a policy to a refined policy using predicted outcomes from `M`.

**Quasi‑reflective equilibrium.** `π* = lfp(F_Act)` under discounting/regularization. Guards: (i) step‑wise delay `next`, (ii) barrier around model invocation, (iii) paraconsistent handling of conflicting value signals.

**Alignment hooks.** Collapse policies act as **normative priors**; edits from the regen affordance `G` (§8) inject constraints when `⋈` appears in value‑critical zones.

---

## Page 15 — Collapse risks and meltdown detectors

**Risks.**

* **Self‑excitation** loops (`M` trusting its own output unguarded) → oscillation.
* **Belief collapse**: unlimited `↓` across levels.
* **Paradox amplification**: unbarriered Liar‐like constructs.

**Detectors.**

* **Spectral radius** of the linearized operator `DF|_*`; if ≥1, throttle with increased delay.
* **Zone‑flux** measure: rate of cross‑zone dependencies; cap flux per step.
* **Tension volume** `|C_Z|` growth; if superlinear, trigger policy intervention.

---

## Page 16 — Algorithms for reflexive evaluation

1. **Zone planning.** Partition computations; put self‑model calls in child zones.
2. **Guard insertion.** Transform recursion to pass through `next` or barriered constructors.
3. **Approximation ladder.** Evaluate with step index `k=0,1,2,…`; stop on stability metric.
4. **Collapse control.** If `⋈` detected in critical zones, run policy selection; otherwise keep paraconsistent.
5. **Regen sweep.** Apply `T=R∘U` to canonicalize scenes; log edits and gap budgets.

Complexity: per unfold cost plus model query cost; parallelizable across zones.

---

## Page 17 — Worked examples I (recursive definitions)

**Stream of locations.**

```
path ≔ Y▸ (λf:▷Path→Path. cons(here, next f))
```

Produces an infinite (coinductive) path, observable up to `k` steps.

**Graph reachability.**

```
Reach(x,y) ≔ μX. (x=y) ∨ ∃z (R(x,z) ∧ next X(z,y))
```

Guard ensures contractivity; denotation is reflexive‑transitive closure.

---

## Page 18 — Worked examples II (self‑modeling agents)

**Predict‑then‑act.**

```
π₀  : Obs→Dist Act
M    : PolicyObj → OutcomeObj
F_Act(π) ≔ softmax( Utility∘M(π) )
π*   ≔ Y▸ (λp:▷Π→Π. λo. step (F_Act (unbox p)) o)
```

Barriers prevent `M` from consuming `π*` unguarded. Aboutness records a meta‑edge from the agent to its policy object.

**Self‑trust calibration.** Introduce `trans` to flip model perspective (agent vs external). Compare outcomes; if `⋈`, spawn split policies and evaluate credal mix until collapse.

---

## Page 19 — Test harness and verifiable guarantees

**Properties.**

* Guarded recursion termination (approximation soundness).
* Layered Tarski holds for constructors used.
* Tower non‑collapse: no `↓` without certificate.
* Non‑explosion: contradictions remain local.
* Regen idempotence up to ANF.

**Checks.**

* Step‑index stability within ε after N steps.
* Flux and spectral thresholds under control.
* Audit trail for every `↓` and barrier discharge.

---

## Page 20 — Next‑step plan and export schema

1. Implement `Y▸`, `next`, `unbox`, and step‑indexed evaluator with zones.
2. Provide certified channels for `quote/eval/↓` with logs.
3. Build self‑model agent demo: policy fixed point with collapse control and regen sweeps.
4. Release JSON exports for proofs and audits.

**Export schema (JSON).**

```json
{
  "fixpoints": [{
    "name": "policy_fp",
    "operator": "F_Act",
    "guard": "next",
    "zone": "Z_policy",
    "approx_steps": 12,
    "stable": true
  }],
  "barriers": [{
    "term": "eval_ℓ(quote(L))",
    "zone": "Z_liar",
    "status": "anti"
  }],
  "audits": [{
    "event": "downlift",
    "from": "ℓ+1",
    "to": "ℓ",
    "term": "eval_ℓ(q)",
    "certificate": "sha256:…"
  }]
}
```

---

*End of Part III §11: Reflexive Systems & Semantic Paradox (20pp v0.1).*


---

# MetaPrincipia Autopoiētica — Part III: Applications & Executable Interpretants

## §12. Dialogue, Agents, and Knowledge Graphs — Agents as Regen‑Executors; Info‑Autopoiesis in Multi‑Agent Worlds (Twenty‑Page Slab, v0.1)

> **Thesis.** Dialogue is **scene exchange** among agents that **regenerate** and **canonicalize** their internal meanings while preserving aboutness and isolating contradictions. Agents are **regen‑executors**: they apply the monad `T=R∘U` (§8) to incoming utterances and to their own beliefs, expose queries as **selectors** (§9), and coordinate via barrier‑aware protocols (§7) over shared **knowledge graphs**.

**Standing context.** Symbols & kinds (Part I), tri‑layer semantics & `S` (Part II §6), paraconsistent barriers (Part II §7), regen monad (Part II §8), natural language front‑end (Part III §9), mathematics/category (§10), reflexivity (§11).

**Page plan (20):**

1. Agent model & world sketch
2. Message ontology & speech‑act calculus
3. Dialogue → scene translation
4. Agent memory as zone‑sharded KG
5. Regen‑executor loop
6. Selector pipeline (QA as aboutness)
7. Evidence, provenance, authority
8. Paraconsistent interaction across agents
9. Merge/fuse and collapse policies
10. Multi‑agent protocols (ask/tell/challenge)
11. Negotiation & alignment as fixed points
12. CRDT‑style eventual consistency
13. DPO rewriting on KGs
14. Belief revision (AGM‑Z)
15. Safety and meltdown control
16. Algorithms & complexity
17. Worked dialogues
18. Benchmarks & metrics
19. JSON schemas & APIs
20. Next‑step plan

---

## Page 1 — Agent model & world sketch

**World.** A multi‑agent system `𝒲 = ⟨Agents, Env, Channels⟩`.

**Agent `A`.** State `Σ_A = ⟨Bel_A, Des_A, Pol_A, KG_A, Zones_A, Logs_A⟩` where:

* `KG_A` is a typed aboutness hypergraph (knowledge graph).
* `Zones_A` partitions `KG_A` into isolation regions (§7).
* `Pol_A` are policies: collapse, authority, trust, regen budget.
* `Bel_A` maps to `KG_A` views; `Des_A` to goals; `Logs_A` for audits.

**Interfaces.**

* `parse: Text → Scene` (Part III §9).
* `S: Expr → (⟦·⟧_E,⟦·⟧_I,|·|)` (Part II §6).
* `T=R∘U: Scene → Scene` (Part II §8).
* `Barrier/Zone` control (Part II §7).

---

## Page 2 — Message ontology & speech‑act calculus

Messages are **typed scene acts**. Core kinds:

* **Assert(φ, meta)**: propose edges for receiver’s KG.
* **Query(Wh, φ)**: selector over the receiver’s aboutness.
* **Evidence(e)**: attach provenance tokens to edges.
* **Challenge(φ)**: flag `⋈` intent.
* **Policy(π)**: propose collapse/merge rules.
* **Plan(a)**: propose action scene.

**Speech‑act operators.**

```
Tell_A→B(φ)      Ask_A→B(Wh,φ)      Challenge_A→B(φ)
Provide_A→B(e|φ)  Align_A↔B(π)       Commit_A(Plan)
```

Semantics: each act yields a **delta** `Δ` on the receiver’s KG plus queue of follow‑ups.

---

## Page 3 — Dialogue → scene translation

Utterance `u` parsed to `Scene` `H_u`; then `ANF(H_u)` with torsion dictionary `D*`. Attach **speaker** and **time** roles:

```
said(Speaker=A, Content=H_u, Time=t)
```

This yields edges `(A —said@t→ H_u)` and embeds `H_u` into a **message zone** `Z_msg`. The receiver applies `S` and `T` before any merge.

---

## Page 4 — Agent memory as zone‑sharded KG

`KG_A` is sharded by zones:

* `Z_src` per external source.
* `Z_core` for A’s stable core.
* `Z_hyp` for hypotheses.
* `Z_policy` for norms.

Edges carry `zone(e)`, `authority(e)`, `confidence(e)`, `timestamp(e)`. Cross‑zone links are **views** or **fuses** with policy checks.

---

## Page 5 — Regen‑executor loop

On receiving `u` from `B`:

1. `H ← parse(u)` → `ANF(H)`.
2. `κ ← U(H)`; compute `Δ_need = Δ(κ)` (§8).
3. Optionally request evidence or spawn placeholders (regen with low weight).
4. `H′ ← R_π(κ)`; maintain lineage.
5. Insert into `KG_A` under zone `Z_B`.
6. If `Ask`, run **selector** pipeline; if `Tell`, update and maybe reply with `Ack/Evidence`.

`T` ensures canonicalization; budgets control exploratory edits.

---

## Page 6 — Selector pipeline (QA as aboutness)

For `Ask_A→B(Wh,φ)` the receiver B computes `Ans_Wh(φ)` using §9 formula over its `KG_B`. If unknown, B may:

* query other agents, citing A’s request, or
* trigger `G(Δ(U(φ)))` to fill gaps,
* respond with **credal answers** (interval/alternative sets) referencing zones.

Answers are scenes `H_ans` with `about(H_ans) ⊆ about(φ)`.

---

## Page 7 — Evidence, provenance, authority

Edges have **provenance capsules**:

```
prov(e) = {source, method, time, hash, license}
```

Authority score `auth(src)` feeds collapse policy. **Evidence acts** attach capsules; **challenges** may request capsules or dispute them.

Audit guarantees: every collapse decision stores the **policy path** and input capsules.

---

## Page 8 — Paraconsistent interaction across agents

Contradictory assertions create `⋈` inside `Z_src` or `Z_B`. Non‑explosion holds by **zone locality** (§7). Cross‑agent queries must specify **resolution mode**:

* `strict`: only `◦`‑validated edges.
* `credal`: lower/upper bounds.
* `contrastive`: surface both sides with tension markers.

---

## Page 9 — Merge/fuse and collapse policies

When sources align, `fuse⟨Z_i,Z_j⟩` merges zones after policy `π_collapse` chooses `φ` or `¬φ` per `⋈` (Authority/Recency/Minimal‑Change). Resulting zone gains `◦` annotations; logs record decisions and counterfactuals.

**Counterfactual store.** Keep losing alternatives in `Z_alt` for recovery and explanation.

---

## Page 10 — Multi‑agent protocols (ask/tell/challenge)

**Protocol P‑ATC.**

1. `Ask`: A→B, includes `Wh, φ, mode`.
2. `Tell`: B→A with `ans` scene and `prov`.
3. `Challenge`: A→B if inconsistencies with A’s KG; include expected edges.
4. `Evidence`: B→A with capsules or revised collapse; else `Agree/Disagree` scene.

**Termination.** Ends when `mode=strict` answers stabilize or budgets expire; otherwise continue under credal mode.

---

## Page 11 — Negotiation & alignment as fixed points

Model **alignment** as finding a policy fixed point `π*` across agents minimizing disagreement:

```
π_{t+1}^A = F_A(π_t^A, π_t^{−A})
```

where `F_A` updates collapse/merge thresholds from observed gains/losses. Under contraction (step size <1) a Nash‑like fixed point exists. Use **guarded iteration** (`next`) to avoid oscillation.

Payoff = utility of coherent answers on shared tasks − penalties for false collapses.

---

## Page 12 — CRDT‑style eventual consistency

Define per‑zone operations that are **commutative, associative, idempotent**:

* `add_edge(e)`, `add_zone(Z)`, `tag⋈(e)`, `attach_prov(e,p)`.
* `collapse(Z,φ→choice)` is **non‑CRDT**; serialize via **policy logs** and consensus.

Distribute KGs with **causal delivery**; replicas converge on the CRDT subset; collapses reconcile by replaying logs with the same policies.

---

## Page 13 — DPO rewriting on KGs

Use **Double‑Pushout (DPO)** rewriting inside zones to maintain schemas:

* Rules `L ← K → R` match subgraphs and replace while preserving aboutness invariants (§10 adhesivity).
* Examples: `on/atop` synonym collapse; enforcing `Surface(y)` before `on(x,y)`.

Confluence holds per zone if critical pairs join; compute locally with regen passes.

---

## Page 14 — Belief revision (AGM‑Z)

Adapt **AGM** postulates to **zones**:

* **Closure**: revised beliefs form a zone‑closed set.
* **Success**: accept `φ` into some zone unless forbidden.
* **Inclusion**: minimal change measured by Δ on ANF.
* **Vacuity**: if not contradicting, no collapse needed.
* **Consistency**: preserve `◦` in protected zones.

Revision operators:

* `⊕_Z φ` (expansion in zone `Z`),
* `⊖_Z φ` (contraction),
* `*_{π,Z} φ` (revision by collapse under policy `π`).

---

## Page 15 — Safety and meltdown control

**Detectors.**

* Tension growth `|C_Z|` per time slice.
* Collapse churn rate.
* Zone‑flux between `Z_core` and externals.
* Spectral radius of update operators (belief/policy).

**Guards.**

* Hard caps on down‑lifts `↓`.
* Mandatory barriers for self‑reference (§11).
* Budget throttles for regen edits.
* Quarantine zones for hostile inputs.

---

## Page 16 — Algorithms & complexity

**Reception.** `O(|u|)` parse + `O(|E| log |E|)` ANF.
**Merge.** View‑gluing `O(|match|)`; collapse calls `O(|C_Z|)` per zone.

**Selector.** Role‑filtered neighborhood queries near‑linear; intervals require two passes.

**DPO.** Rule matching via VF2 or OS‑CFI; local in zones; amortize with regen caches.

---

## Page 17 — Worked dialogues

**D1. Ask/Tell.**

```
A→B: where( on(Cat,Mat) )?
B: {Mat}  [prov: source=vision#42]
```

**D2. Contradiction.**

```
A: on(Cat,Mat)
C: ¬on(Cat,Mat)
B: stores both in Z_A, Z_C with ⋈; answers credal intervals until collapse.
```

**D3. Negotiation.**

```
A↔B: Align(π: prefer high‑confidence → collapse)
Both apply π; zones fused; future queries strict.
```

---

## Page 18 — Benchmarks & metrics

* **Answer fidelity** vs curated KGs.
* **Paraphrase invariance**: `≈̇` stability under rephrasing.
* **Tension isolation**: fraction of `⋈` not leaking.
* **Consensus latency**: time to strict answers after conflicts.
* **CRDT convergence**: replica divergence over time.

Ablations: regen budget, policy weights, torsion dictionary size.

---

## Page 19 — JSON schemas & APIs

**Message.**

```json
{
  "id":"m#…",
  "from":"A","to":"B","type":"Ask|Tell|Challenge|Evidence|Policy|Plan",
  "content":"…raw text…",
  "scene_id":"s#…","mode":"strict|credal|contrastive",
  "time":"2025-09-18T12:00:00Z"
}
```

**Edge capsule.**

```json
{
  "edge_id":"e#…",
  "zone":"Z_src",
  "relator":"on",
  "roles":{"Theme":"cat#1","Surface":"mat#1"},
  "prov":{"source":"vision#42","hash":"sha256:…","license":"CC-BY"},
  "confidence":0.92,
  "tension":false
}
```

**Collapse log.**

```json
{
  "zone":"Z_A∪Z_C",
  "formula":"on(cat#1,mat#1)",
  "decision":true,
  "policy":"Authority+Recency",
  "inputs":["e#…","e#…"],
  "counterfactual_zone":"Z_alt#7",
  "time":"…"
}
```

**Selector API.**

```json
POST /ask
{ "Wh":"where", "phi":"on(cat, mat)", "mode":"credal" }
```

---

## Page 20 — Next‑step plan

1. Implement zone‑sharded KG with ANF, DPO rules, and CRDT ops.
2. Build P‑ATC protocol over a message bus with provenance capsules.
3. Add policy engine for collapse and alignment fixed‑point iteration.
4. Release evaluation suite: tension isolation, consensus latency, QA fidelity.

---

*End of Part III §12: Dialogue, Agents, and Knowledge Graphs (20pp v0.1).*
