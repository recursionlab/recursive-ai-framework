# MetaPrincipia Autopoiētica — ADD‑ONS

## Appendix A — Regen Coherence Proofs (Twenty‑Page Slab, v0.1)

> **Objective.** Prove that the **regen operator** `T = R∘U` (compress‑then‑rebuild) is a lawful, safe, and compositional normalization for scenes, selectors, and interpreters. We establish: (i) categorical construction via an adjunction `U ⊣ R`, (ii) monad laws and near‑idempotence, (iii) coherence with relators, selectors, meta‑relators, and effects, (iv) termination and confluence of the rewrite system realizing `T`, and (v) preservation of aboutness and paraconsistent isolation.

**Context prerequisites.** Part I (symbol system, kinds, formation), Part II §5–§8 (aboutness, axioms, barriers, paraconsistency, regen), Part III §9–§12 (language↔KG), Part IV §13–§16 (grounding, meta‑interpretation, ARC, autopoiesis).

**Page map (20):**

1. Setup and notations
2. Categories `Scene` and `Code`
3. Adjunction `U ⊣ R` and monad `T`
4. Monad laws and KZ‑idempotence
5. Monoidal coherence with relator tensor
6. Selector coherence (questions commute)
7. Denotational coherence (E/I/|·| layers)
8. Distributive law with interpreter effects
9. Rewrite system ℛ\_T: rules and orientation
10. Termination by multivariate measure
11. Local confluence via critical pairs
12. Global confluence (Newman / decreasing diagrams)
13. DPO graph rewriting compatibility
14. Meta‑relator coherence
15. Tower and zone safety
16. Preservation theorems (types, roles, aboutness)
17. Counterexamples and necessity of assumptions
18. Algorithms and certificates
19. JSON schemas for proofs & audits
20. Next‑step plan

---

## Page 1 — Setup and notations

* Let `Scene` be the category of well‑typed aboutness hypergraphs with role‑labeled hyperedges and zone annotations; arrows are structure‑preserving maps.
* Let `Code` be the category of canonical **codes** (ANF) with torsion dictionaries `D*`; arrows are code homomorphisms.
* `U : Scene → Code` (**understand**) extracts codes; `R : Code → Scene` (**rebuild**) reifies codes into canonical scenes.
* Define `T = R∘U : Scene → Scene`. We write values `⟦·⟧_E, ⟦·⟧_I, |·|` as in Part II §6.
* Scene tensor `⊗` composes disjoint subscenes; unit `I` is empty scene. Zones are written `Z ⊲ s`.

---

## Page 2 — Categories `Scene` and `Code`

**Assumption A.1 (adhesive fragment).** `Scene` has monos stable under pushout; pushouts along monos exist. `Code` is a finitary algebraic category with finite limits and pushouts.

**Lemma 2.1.** There is a faithful functor `J : Scene → Str(SIT)` (Part IV §13) mapping scenes to situation structures; `J` preserves monos and pushouts in the declared fragment.

*Sketch.* Roles as typed incidence; edges as relation symbols; adhesivity standard.

---

## Page 3 — Adjunction `U ⊣ R` and monad `T`

**Definition.** `U` forgets graph sharing and records a code with torsion facts; `R` realizes a code by reifying anchors and edges under `D*`.

**Theorem 3.1 (Adjunction).** `U ⊣ R` with unit `η : Id_Scene ⇒ R∘U` and counit `ε : U∘R ⇒ Id_Code`.

*Proof sketch.* `U` universal for maps from a scene to a code factoring canonicalization; `R` right adjoint by evaluation of codes in scenes; triangle identities hold by code realization laws.

**Corollary 3.2.** `T = R∘U` is a monad with `η` as unit and `μ = R ε U` as multiplication.

---

## Page 4 — Monad laws and KZ‑idempotence

**Theorem 4.1 (Monad laws).** `μ ∘ Tη = id_T = μ ∘ ηT` and associativity `μ ∘ Tμ = μ ∘ μT`.

*Proof.* Immediate from the adjunction: triangle identities entail monad laws.

**Proposition 4.2 (Kock‑Zöberlein / idempotence).** If `R` is full and faithful on the image of `U` (codes realize to unique canonical scenes), then `T` is an **idempotent (KZ)** monad: there is an iso `ι: TT ⇒ T` compatible with `η, μ`.

*Consequence.* One regen pass equals any finite number up to isomorphism: `T(T(s)) ≅ T(s)`.

---

## Page 5 — Monoidal coherence with relator tensor

**Theorem 5.1.** `U` and `R` are **strong monoidal** on the symmetric monoidal structures `(Scene, ⊗, I)` and `(Code, ⊕, 0)` with coherence maps `φ^U, φ^R` providing natural isos:

```
U(s ⊗ t) ≅ U(s) ⊕ U(t),   U(I) ≅ 0
R(c ⊕ d) ≅ R(c) ⊗ R(d),   R(0) ≅ I
```

Hence `T` is a **strong monoidal endofunctor** on `Scene`.

*Proof sketch.* Disjoint composition factors through code concatenation and vice versa; unit laws are immediate; coherence via Mac Lane pentagon/triangle holds by construction of `φ`.

**Corollary 5.2 (Relator coherence).** For relator‑mediated composition inside scenes, `T` preserves tensor up to the coherence isos, so bracketing differences normalize to the same ANF.

---

## Page 6 — Selector coherence (questions commute)

Let `Sel : Scene → Ans` be the **selector functor** (Part III §9) that answers interrogatives by role‑filtered queries over scenes.

**Theorem 6.1 (Selector naturality).** There exists a natural iso `σ : Sel∘T ⇒ Sel` on the well‑typed fragment where `U` records exactly the anchors relevant to the selector.

*Proof.* `U`/`R` preserve incident role structure; `Sel` depends only on that structure. Construct `σ_s : Sel(T(s)) → Sel(s)` as the identity on the anchor/role projection.

*Consequence.* Asking questions after regen yields the same answers as asking before, up to canonical identifier isomorphism.

---

## Page 7 — Denotational coherence (E/I/|·| layers)

Define projections of semantics (Part II §6): `⟦·⟧_E : Scene→2`, `⟦·⟧_I : Scene→(W→2)`, `|·| : Scene→Hyp`.

**Theorem 7.1 (Extensional preservation).** If `U` records only equivalence‑preserving torsions and `R` realizes them soundly, then `⟦T(s)⟧_E = ⟦s⟧_E`.

**Theorem 7.2 (Intensional preservation).** For Kripke‑monotone torsions, `⟦T(s)⟧_I(w) = ⟦s⟧_I(w)` for all worlds `w`.

**Theorem 7.3 (Aboutness invariance).** There is a natural iso `κ : |T(s)| ≅ |s|` given by the identity on anchors and role‑preserving relabeling of reified edges.

*Proof sketches.* `U`/`R` do not alter truth conditions; they reorganize structure. Aboutness iso is by hypergraph isomorphism preserving incidence.

---

## Page 8 — Distributive law with interpreter effects

Interpreters compute in a monad `Eff` (Part IV §14). We define a **distributive law** `λ : T Eff ⇒ Eff T` by pushing regen through effects while preserving logs and tension:

```
λ_X : T(Eff X) → Eff(T X)
```

constructed componentwise as `R(U(State→…)) ≅ State→…` using the strong monoidality and handler naturality.

**Theorem 8.1 (Beck coherence).** If handlers are structure‑respecting (they do not invent edges beyond `U`’s codes without budget) and barrier‑safe, then `λ` satisfies Beck’s four axioms; hence `Eff∘T` lifts to a composite monad.

*Consequence.* We may **interpret‑then‑regen** or **regen‑then‑interpret** with equal observable results up to audit log isomorphism.

---

## Page 9 — Rewrite system ℛ\_T: rules and orientation

Let ℛ\_T be the presentation of `T` as a terminating, confluent rewrite to ANF. Rules (selected):

1. **Relator flattening.** Nested associative compositions → right‑canonical spine.
2. **Role normalization.** Swap to canonical role order.
3. **Torsion resolution.** Declared synonymy (`on/atop`) collapses via oriented rewrite guarded by predicates (e.g., `Surface`).
4. **Meta‑lift hoist.** Move admissible meta‑operators to header positions.
5. **Zone‑respect.** Rewrites never cross zone boundaries; instead, introduce **view nodes**.

**Design choice.** Associativity is treated as **equational**; orientation only applies to nested spines of bounded schema to avoid non‑termination.

---

## Page 10 — Termination by multivariate measure

Define a **well‑founded measure** `M : Scene → 𝔑^4` ordered lexicographically with **multiset** refinement:

```
M(s) = ⟨ m₁(s), m₂(s), m₃(s), m₄(s) ⟩
```

where

* `m₁` = count of **mis‑nested meta** operators (non‑header meta occurrences).
* `m₂` = multiset of **spine heights** of relator chains not in canonical right form, ordered by multiset extension.
* `m₃` = count of **role inversions** relative to dictionary order.
* `m₄` = count of **unresolved torsions**.

**Lemma 10.1.** Each rule in ℛ\_T strictly decreases `M`.

*Note on para‑through.* The problematic rule `(para‑through(R,S))∘T ↦ para‑through(R, S∘T)` is **not** used as a rewrite. Instead, `para‑through` associativity is **equational** and normalized by a separate *canonical bracketing* function whose cost does not appear in ℛ\_T. Hence constructor depth cannot increase along ℛ\_T reductions.

**Theorem 10.2 (Termination).** No infinite ℛ\_T reduction exists.

---

## Page 11 — Local confluence via critical pairs

Compute overlaps between left‑hand sides of rules ignoring zone boundaries. For each critical pair, either:

* the overlap is impossible by typing/guards, or
* the pair **joins** after ≤2 rewrites due to common right‑canonical targets (role order and meta‑hoist are orthogonal).

**Lemma 11.1.** ℛ\_T is locally confluent.

---

## Page 12 — Global confluence (Newman / decreasing diagrams)

Since ℛ\_T terminates (Thm 10.2) and is locally confluent (Lem 11.1), **Newman’s Lemma** gives **confluence**. Alternatively, construct **decreasing diagrams** using `M` to label peaks; every peak decreases.

**Corollary 12.1.** Every scene reduces to a **unique ANF** up to isomorphism and zone‑renaming.

---

## Page 13 — DPO graph rewriting compatibility

**Theorem 13.1.** `T` **commutes with DPO** rewriting along monos in the adhesive fragment:

```
T ∘ Rewr_{L←K→R}  ≅  Rewr_{L←K→R} ∘ T
```

*Proof sketch.* `U` preserves monos and pushouts; `R` creates pushouts from code pushouts; thus the square that defines DPO matches through `U` and `R`.

**Consequence.** Schema maintenance (e.g., `on` requires `Surface`) may be expressed by DPO rules without fighting the regen normalizer.

---

## Page 14 — Meta‑relator coherence

Let `MRel` be meta‑relators acting as endofunctors on `RelCat`. Assume **liftability**: `U∘meta ≅ meta∘U` on the declared fragment.

**Theorem 14.1.** `T` commutes with meta‑relators up to iso:

```
T(meta·e) ≅ meta·T(e)
```

*Proof.* From liftability and `R` realization naturality. For `anti⟨·⟩`, `T` leaves barrier markers unchanged (rule 5).

---

## Page 15 — Tower and zone safety

**Theorem 15.1 (Tower safety).** `T` preserves level indices; it never introduces `↓` or crosses levels. Hence it cannot cause meta‑level collapse.

**Theorem 15.2 (Zone non‑explosion).** `T` does not merge zones or discharge barriers; contradictions `⋈` stay local.

*Proofs.* Rules never create cross‑zone edges; `U` collapses only **within** zones; `R` reifies per‑zone; logs record all changes.

---

## Page 16 — Preservation theorems (types, roles, aboutness)

**Thm 16.1 (Type preservation).** If `Γ ⊢ s : Scene`, then `Γ ⊢ T(s) : Scene`.

**Thm 16.2 (Role preservation).** Incidence functions for each relator edge are preserved up to canonical permutation.

**Thm 16.3 (Aboutness bisimulation).** The relation `~_T` defined by `s ~_T t ⇔ T(s)=T(t)` is a bisimulation for the call‑by‑meaning small step: if `s ~_T t` and `s ↦ s′`, then there exists `t′` with `t ↦ t′` and `s′ ~_T t′`.

*Consequences.* Operational answers and denotations are unchanged by `T` (cf. Thm 6.1/7.1/7.2).

---

## Page 17 — Counterexamples and necessity of assumptions

* Dropping **guarded meta‑hoist** can re‑introduce the para‑through divergence; termination fails.
* Allowing `U` to invent anchors breaks extensional preservation (Thm 7.1).
* Letting `R` cross zones breaks paraconsistent isolation (Thm 15.2).
* If `U∘R ≄ Id_Code`, KZ‑idempotence does not hold; repeated regen may drift. Guard with equality proofs or proof‑carrying code hashes.

---

## Page 18 — Algorithms and certificates

**Normalizer.** Implement ℛ\_T with rule priorities `meta‑hoist → role‑order → torsion → spine`. Maintain `M` to assert decreases.

**Certificates.** Emit a **regen certificate** containing: (i) input hash, (ii) output hash, (iii) rule trace, (iv) `M` sequence strictly descending, (v) selector check `Sel(T(s))≈Sel(s)`, (vi) zone audit. Auditors recompute or spot‑check.

**Complexity.** Linear‑near‑linear in edges with small constant factors for role/torsion checks; DPO compatibility adds pattern‑match cost where used.

---

## Page 19 — JSON schemas for proofs & audits

**Regen certificate.**

```json
{
  "input_scene_hash": "sha256:…",
  "output_scene_hash": "sha256:…",
  "rules": [
    {"id":"meta-hoist","before":"…","after":"…"},
    {"id":"role-order","before":"…","after":"…"}
  ],
  "measure": [
    {"m1":7, "m2":[3,2], "m3":4, "m4":6},
    {"m1":5, "m2":[3,1], "m3":3, "m4":6}
  ],
  "selector_check": {"passed": true},
  "zone_audit": {"cross_zone_updates": 0}
}
```

**Adjunction witness.**

```json
{
  "U⊣R": {
    "unit_eta": "proof#…",
    "counit_eps": "proof#…",
    "triangles": true
  }
}
```

**Distributive law λ.**

```json
{
  "lambda": {
    "type": "T∘Eff ⇒ Eff∘T",
    "beck_axioms": ["nat","mult","unit","compat"],
    "handler_family": ["state","prov","policy","regen"],
    "barrier_safe": true
  }
}
```

---

## Page 20 — Next‑step plan

1. Ship a reference ℛ\_T implementation with descending‑measure certificates and optional decreasing‑diagrams audit.
2. Provide proof objects for the adjunction and KZ‑idempotence claims.
3. Release selector regression tests demonstrating `Sel∘T ≅ Sel`.
4. Add DPO compatibility harness and meta‑relator commuting tests.
5. Integrate into interpreter stack with distributive law `λ` and barrier checks; expose APIs for regen certificates.

---

*End of Appendix A — Regen Coherence Proofs (20pp v0.1).*


---

# MetaPrincipia Autopoiētica — ADD‑ONS

## Appendix B — Aboutness Compression Algorithms (Twenty‑Page Slab, v0.1)

> **Objective.** Design and analyze algorithms that **compress aboutness** representations `|t|` (role‑labeled hypergraphs) while preserving *semantic utility*: selector answers, coherence constraints, regen compatibility, and paraconsistent isolation. We give lossless and lossy schemes with provable guarantees, certificates, and APIs.

**Dependencies.** Part I (symbol system), Part II §5–§8 (aboutness, axioms, barriers, regen), Part III §9–§12 (selectors, dialogue, KGs), Part IV §13–§16 (grounding, interpreters, emergence, autopoiesis). Appendix A (Regen coherence).

**Page map (20).**

1. Scope and invariants
2. Data model and query family
3. Utility metrics and budgets
4. Lossless canonicalization (AC‑0)
5. Role‑aware hashing & dedup (AC‑1)
6. Motif dictionaries (AC‑2)
7. Hypergraph sparsification (AC‑3)
8. Low‑rank tensor models (AC‑4)
9. Semantic MinHash & sketches (AC‑5)
10. Information Bottleneck (AC‑6)
11. MDL normalization (AC‑7)
12. DPO summarization (AC‑8)
13. Paraconsistent packing (AC‑⋈)
14. Selector‑Lipschitz guarantees
15. Regen compatibility and commuting diagrams
16. Algorithms and complexity
17. Worked examples
18. Certificates and audits
19. JSON interchange
20. Next‑step plan

---

## Page 1 — Scope and invariants

**Aboutness object.** `|t| = H = ⟨V, E, ι, ρ, Z⟩` where `V` anchors, `E` hyperedges, `ι:E→V^k` incidences, `ρ` role labels, `Z` zones.

**Invariants.**

* **I‑Sel.** Answers to declared selector families are preserved up to policy tolerances.
* **I‑Role.** Role incidence preserved or mapped by a recorded permutation.
* **I‑Coherence.** Declared constraints hold (e.g., `Surface` before `on`).
* **I‑Regen.** Commutes with `T = R∘U` (Appendix A).
* **I‑Par.** `⋈` markers and barriers remain local; no unintended merges.

Compression aims to minimize a size functional `C(H)` subject to these invariants and budgets.

---

## Page 2 — Data model and query family

**Selectors as queries.** We consider a finite family `𝒬` of role‑filtered neighborhood queries and path queries of radius `r`:

```
where(φ) , who(φ), what(φ) , count(ψ) , reach(ψ;≤L)
```

Each query `q∈𝒬` is evaluated by graph operations on `H`.

**Admissible losses.** An `(ε,δ)`‑compressor may alter answers with probability ≤δ and numeric error ≤ε under a test distribution. For strict mode, ε=δ=0.

---

## Page 3 — Utility metrics and budgets

Define utility at query granularity:

```
U(H;𝒬) = 1/|𝒬| Σ_q u(Ans_q(H), Ans_q(H_ref))
```

with `u` a per‑query scorer (exact match, F1, ±tol). Track:

* **Budget\_Bits** = target size.
* **Budget\_Err** = allowed aggregate ΔU.
* **Budget\_Time** for online compression.

Compression problem: minimize `C(H′)` s.t. `U(H′;𝒬) ≥ τ`, invariants hold, and `H′` encodes provenance.

---

## Page 4 — Lossless canonicalization (AC‑0)

**AC‑0 (ANF).** Apply regen `T` to obtain **A**‑**N**ormal **F**orm. This is *lossless* and required before any lossy step. Effects:

* Deduplicate isomorphic subscenes modulo torsion.
* Canonicalize role orders and spines.
* Split zones and insert view nodes.

**Guarantee.** `Sel(T(H)) ≅ Sel(H)`; see Appendix A.

---

## Page 5 — Role‑aware hashing & dedup (AC‑1)

**Idea.** Use **Weisfeiler–Lehman (WL)** color refinement extended to **role‑labeled hypergraphs** to obtain stable fingerprints for edges and small subgraphs.

**Algorithm.**

1. Initialize color of each edge by `(relator, role‑multiset, zone)`; node by `(type, zone)`.
2. Iterate: recolor by hashing neighbor color multisets stratified by roles.
3. Merge exact‑match subgraphs (same fingerprints, same capsules) to a single representative; keep multiplicity.

**Loss model.** Lossless if we do not merge across capsules; lossy if we allow synonymy via torsion dict.

**Complexity.** `O((|V|+|E|) log |V|)` per round; few rounds.

---

## Page 6 — Motif dictionaries (AC‑2)

**Idea.** Replace frequent subgraphs with **motif symbols** and a dictionary.

**Procedure.** Mine subgraphs with WL fingerprints above support `s`; enforce role‑isomorphism. Build a **dictionary** `D = {m_i ↦ pattern_i}` and an **encoding** that replaces instances by `m_i` references.

**Guarantees.** Lossless if expansion is exact; selector‑safe if queries can be answered on motifs using **summary predicates** stored with `m_i` (e.g., exposed boundary roles, counts, reachability summaries).

**Benefit.** Reduces storage; improves locality for query execution.

---

## Page 7 — Hypergraph sparsification (AC‑3)

**Goal.** Keep a small subset of edges `E′⊆E` that preserves answers to cut‑like and neighborhood queries.

**Method.**

* Build **role‑aware incidence matrix** or tensor.
* Compute **effective resistances** on the star‑expansion graph or use hypergraph spectral sparsification (approximate) with sampling probabilities proportional to leverage scores.
* Reweight retained edges.

**Guarantee.** For any cut query induced by roles, volumes preserved within `(1±ε)`. For count/selectors in `𝒬`, derive bounds from cut preservation.

**Notes.** Respect zones: sample per zone; never drop `⋈` edges by default.

---

## Page 8 — Low‑rank tensor models (AC‑4)

**Setup.** Incidence encoded as a sparse **order‑k tensor** `𝒯` with role modes. Apply **CP/Tucker** factorization under nonnegativity and role constraints.

**Compression.** Store factors `(A₁,…,A_k)` with rank `r≪|V|`; approximate edges by reconstructed high‑value entries.

**Selector safety.** Provide **guard intervals**: if reconstruction confidence below τ on a queried incidence, fall back to dictionary/motif expansion or original edges.

**Guarantee.** For count queries, relative error bounded by reconstruction error; for reachability, use hybrid execution: exact on skeleton + estimated on low‑rank fill within δ.

---

## Page 9 — Semantic MinHash & sketches (AC‑5)

**Idea.** Create **role‑edge shingles** (e.g., `(relator,role,node‑color)` tuples) and compute MinHash signatures per anchor or zone to estimate Jaccard similarities and to cluster.

**Use.**

* Fast paraphrase detection (≈̇ candidates).
* Candidate merges before exact WL test.
* Similarity search across agents (§12) with small sketches.

**Loss.** Only for similarity; selectors rely on exact structures after shortlist.

---

## Page 10 — Information Bottleneck (AC‑6)

**Goal.** Learn compressed codes `Z` that retain maximal information about selector answers `Y=Sel(H)` while compressing `H`.

**IB objective.**

```
max  I(Z; Y) − β I(Z; H)
```

Parameterize `p(Z|H)` with graph neural encoders constrained to be **role‑equivariant** and **zone‑aware**. Decode selectors from `Z`. Adjust β to meet budgets.

**Guarantees.** Empirical; provide **calibration** and **coverage** reports; backstop with strict fallbacks for high‑risk queries.

---

## Page 11 — MDL normalization (AC‑7)

**Minimum Description Length.** Choose among models `M` (motif+sketch+sparse+low‑rank) the one minimizing

```
L(H, M) = L(M) + L(H | M)
```

subject to invariants and selector constraints. Penalize violations heavily. Supports **automatic model selection** and adaptive compression.

---

## Page 12 — DPO summarization (AC‑8)

Apply **Double‑Pushout** graph rewriting to enforce schemas and fold redundant patterns:

* Collapse synonym relators (`on/atop`) under guards.
* Introduce **summary nodes** for repeated role patterns.
* Maintain **adhesive** conditions for confluence.

Produces a smaller, schema‑consistent `H′` that is ANF by construction.

---

## Page 13 — Paraconsistent packing (AC‑⋈)

**Problem.** Contradictory edges must not explode but must remain **addressable**.

**Solution.**

* Pack `⋈` subgraphs into **tension capsules** with boundary summaries.
* Do not merge across `⋈` by WL unless *both* sides hash equally **and** capsule IDs match.
* Selectors default to **credal** answers using capsule summaries; strict mode requires collapse policies (§7, §12).

---

## Page 14 — Selector‑Lipschitz guarantees

Define a metric `d(H,H′)` (e.g., weighted edit distance respecting roles and zones). A compressor is **selector‑Lipschitz** with constant `L_q` for query `q` if

```
|u(Ans_q(H), Ans_q(H′)) − 1| ≤ L_q · d(H,H′)
```

**Theorem (Sketch).** AC‑3 sparsifiers are selector‑Lipschitz for count queries with `L_q = O(ε)`; AC‑2 motif replacement is Lipschitz with `L_q=0` if boundary summaries are exact; AC‑4 low‑rank yields `L_q≤f(‖𝒯−𝒯̃‖)`.

---

## Page 15 — Regen compatibility and commuting diagrams

**Claim.** For AC‑i that respect ANF boundaries and zones, compression **commutes** with regen:

```
T ∘ AC_i ≅ AC_i ∘ T
```

Construct natural isos using Appendix A’s strong monoidality and selector naturality. For learned compressors (AC‑6), require handlers that **do not invent edges** beyond a logged budget; provide `anti` previews.

---

## Page 16 — Algorithms and complexity

**Pipeline.**

1. AC‑0 ANF.
2. AC‑1 WL dedup.
3. Branch: AC‑2 motifs; AC‑3 sparsify; AC‑4 low‑rank; AC‑5 sketches; optional AC‑6 IB.
4. AC‑8 DPO summarization; AC‑⋈ packing.
5. Emit certificates.

**Complexities (typical).**

* AC‑1: near‑linear.
* AC‑2: subgraph mining NP‑hard; use bounded radius and WL.
* AC‑3: near‑linear sampling.
* AC‑4: `O(r · nnz(𝒯))` per ALS step.
* AC‑5: linear in shingles.
* AC‑6: training cost; inference linear.

---

## Page 17 — Worked examples

**W1 — Spatial scenes.** Dedup parallel `on(x, shelf)` edges; motif for stack; cut‑sparsify lateral relations; selectors unchanged.

**W2 — Dialog graphs.** Motif for `Ask→Tell→Evidence`; MinHash clusters paraphrases; DPO enforces schema; tension capsules pack disputes.

**W3 — KB alignment.** Low‑rank compresses incidence; fallback to motifs on uncertain answers; QA fidelity ≥ τ.

---

## Page 18 — Certificates and audits

Emit **compression certificates**:

* Input/output hashes.
* Invariants satisfied.
* Selector regression scores.
* WL fingerprints and merges.
* Sparsifier ε and sample sizes.
* Low‑rank error norms.
* DPO rule applications.
* Tension capsule inventory.
* Commutation check with `T` on a sample.

Auditors replay with random seeds and spot‑check queries.

---

## Page 19 — JSON interchange

**Compressed pack.**

```json
{
  "anf_hash": "sha256:…",
  "wl": {"colors": "…", "merges": ["e#12→e#7"]},
  "motifs": {"dict": [{"id":"m#stack","pattern":"…","boundary":{"roles":["Theme","Surface"]}}],
             "uses": [{"m":"m#stack","sites":["S1","S3"]}]},
  "sparsifier": {"epsilon": 0.08, "kept": 1243},
  "lowrank": {"rank": 64, "err": 0.11},
  "sketch": {"k": 128, "seed": 1337},
  "dpo": [{"rule":"on→contact","count": 37}],
  "tension": {"capsules": 5},
  "cert": "cert#…"
}
```

**Certificate.**

```json
{
  "cert": {
    "input": "sha256:…", "output": "sha256:…",
    "Sel_regression": {"where": 1.0, "count": 0.98},
    "invariants": {"role": true, "coherence": true, "paraconsistency": true},
    "commutes_with_T": true,
    "notes": "AC‑1+AC‑2+AC‑3 pipeline"
  }
}
```

---

## Page 20 — Next‑step plan

1. Implement AC‑0..AC‑5 as a reference pipeline with certificates.
2. Add AC‑6 IB encoder with selector‑aware losses and strict fallbacks.
3. Integrate DPO rules (AC‑8) per schema.
4. Build audit harness: selector regression, regen commutation, paraconsistent checks.
5. Release open tasks and datasets with intervention scripts and scoring tools.

---

*End of Appendix B — Aboutness Compression Algorithms (20pp v0.1).*


---


# MetaPrincipia Autopoiētica — ADD‑ONS

## Appendix C — Agent‑Based Interpretation Framework (Twenty‑Page Slab, v0.1)

> **Objective.** Specify an executable, safety‑guarded framework for **agents** that interpret, produce, exchange, and reconcile scenes in the calculus 𝒞\_A. We define agent state, effectful interpreters, dialogue acts, merge/consensus protocols, paraconsistent isolation, grounding hooks, regen coherence, and audits. We provide laws, rules, algorithms, and schemas suitable for reference implementations.

**Dependencies.** Part I (symbol system), Part II §5–§8 (aboutness, recursive axioms, barriers, regen), Part III §9–§12 (language, KGs, agents), Part IV §13–§16 (grounding, meta‑interpretation, ARC, autopoiesis). Appendix A (Regen coherence), Appendix B (Aboutness compression).

**Page plan (20):**

1. Agent model overview
2. Agent state and types
3. Interpreter stack per agent
4. Dialogue act calculus
5. Commitment logic and sequent rules
6. Channel model and transport
7. Merge protocol (CRDT + DPO)
8. Paraconsistent isolation across agents
9. Grounding protocols in multi‑agent settings
10. Regen & compression in the loop
11. Trust, identity, and provenance
12. Planning & control loop
13. Learning in agents (policy + interpreter)
14. Multi‑agent algorithms
15. Worked examples
16. Metrics & evaluation
17. Failure modes & guards
18. JSON APIs and capsules
19. Reference pseudocode
20. Next steps

---

## Page 1 — Agent model overview

An **agent** `A` is ⟨`KG, Int, Pol, Keys, Cap, Env`⟩ with:

* `KG` zone‑typed aboutness hypergraph (knowledge base).
* `Int` effectful interpreter stack (§14) with handlers.
* `Pol` policies (answering, merge, collapse, actuation).
* `Keys` identity and signing keys.
* `Cap` capabilities (sensors, effectors, budgets).
* `Env` channels (observe/act/declare).

Agents exchange **capsules** carrying scenes, queries, evidence, or policies. All operations are **barrier‑aware** and **regen‑coherent**.

---

## Page 2 — Agent state and types

**Types.**

```
Agent      ::= ⟨KG, Int, Pol, Keys, Cap⟩
Scene      ::= Hyp with roles, zones, capsules
Message    ::= DA | SceneCapsule | Query | Evidence | Policy
DialogueAct (DA) ::= Assert φ | Ask Q | Answer A | Commit φ | Retract φ | Propose R | Agree R | Disagree R | Proof Π
Capsule    ::= {payload, provenance, zone, signatures}
```

**Judgments.**

```
A ⊢ e ⇓ v ▷ A′           // run e under Int; result v; updated agent A′
A ⊢ msg ▷ A′, outbox      // handle a message; may emit replies
A ⊢ φ ▣ Z                 // φ holds for agent A within zone Z (credal if ⋈)
```

---

## Page 3 — Interpreter stack per agent

Each agent instantiates `Eff` with rows `{state, prov, ⋈, policy, regen, net}`. The **net** operations:

```
send    : Msg → Eff 1
receive : Eff Msg
clock   : Eff Time
```

Handlers are ordered: `prov ≺ state ≺ policy ≺ regen ≺ net`. Regen uses Appendix A `T = R∘U`; compression uses Appendix B AC‑i.

**Law (stack coherence).** Handlers commute pairwise on the core fragment; logs are stable under reorderings that respect precedence.

---

## Page 4 — Dialogue act calculus

Dialogue acts (DAs) are typed transformations on `KG` and **commitment stores** `Cmt`.

**Typing.**

```
Γ ⊢ φ:Prop    Γ ⊢ Q:Question    Γ ⊢ Π:Proof(φ)
```

**Operational rules (selected).**

```
[Assert]   recv(Assert φ)  ⇒  add φ to KG^Z_say with capsule; mark source
[Ask]      recv(Ask Q)     ⇒  run selector; respond Answer A with caps
[Answer]   recv(Answer A)  ⇒  integrate as evidence; attach zone Z_src
[Commit]   recv(Commit φ)  ⇒  add φ to Cmt with signer; derive obligations
[Retract]  recv(Retract φ) ⇒  weaken obligations; add ¬φ to Z_src
[Proof]    recv(Proof Π)   ⇒  check; if OK then elevate φ to strict zone
```

Acts can be **tentative** (zone `Z_src`) or **strict** (zone `Z_strict`) based on policy and proof.

---

## Page 5 — Commitment logic and sequent rules

A **commitment store** `Cmt` is a ledger of agent‑indexed assertions with modalities `{tentative, strict, obligation}`.

**Sequents.** `Γ; Cmt ⊢_A φ @Z` means agent A derives φ in zone Z given KG and commitments.

Rules (selected):

```
(Commit-Intro)   sig_A(φ) ⇒ Γ; Cmt∪{A:φ} ⊢_A φ @Z_strict
(Ask-Answer)     Γ ⊢ where(ψ)=x  ⇒ Γ;Cmt ⊢_A loc(x) @Z
(Obligation)     A:φ → should(A,φ)    (policy‑dependent)
(Paraconsistent) φ, ¬φ @Z_src ⇒ no explosion; marks ⋈
```

**Soundness.** With honest signatures and verified proofs, strict commitments reflect facts in `KG`’s strict zones.

---

## Page 6 — Channel model and transport

Channels provide authenticated, ordered delivery with optional broadcast. Messages carry:

```
⟨msg_id, sender, receiver(s), payload, time, zone, signatures, hash⟩
```

Policies control rate limits, maximum unresolved `⋈`, and collapse thresholds. Timeouts produce **negotiation** acts: `Propose`, `Agree`, `Disagree` on resolutions.

**Security.** Ed25519 signatures; content hashes; optional encryption per zone.

---

## Page 7 — Merge protocol (CRDT + DPO)

Agents maintain `KG` by **CRDT** merges for additive info and **DPO** (double‑pushout) rewriting for schema maintenance.

**CRDT core.**

* **GSet** for anchors and edges (add‑only).
* **OR‑Set** for mutable attributes with tombstones.
* Version vectors per zone.

**DPO rules.** Enforce constraints (`contact` for `on`, etc.). Apply after CRDT merge within each zone; conflicts become `⋈` capsules.

**Merge algorithm.**

1. Apply regen `T` then compression AC‑i to payload.
2. CRDT‑merge per zone; update version vectors.
3. Run DPO schema rules; mark `⋈` conflicts.
4. Optional **collapse** by policy with audit.

---

## Page 8 — Paraconsistent isolation across agents

**Isolation law.** `⋈` markers remain local to **source zones**; merges never fuse contradictory edges into strict zones without explicit **collapse** decisions.

**Barrier ops.** `anti⟨·⟩` to preview merges; `quarantine(Z)` to freeze zones; `fuse⟨Z_i,Z_j⟩` with policy proofs to collapse.

**Guarantee.** Queries across agents default to **credal** answers unless strict evidence dominates by policy.

---

## Page 9 — Grounding protocols in multi‑agent settings

Agents can ground assertions via shared protocols `Pr` (§13). Multi‑agent twist:

* **Role split.** One agent acts; others observe.
* **Cross‑validation.** Majority or trust‑weighted acceptance.
* **Capsule union.** Evidence capsules combined; disagreements stay in `⋈` capsules.

**Grounded act.** `Proof Π` may package protocol transcripts; if verified, promotes to `Z_strict`.

---

## Page 10 — Regen & compression in the loop

Every inbound/outbound scene passes through `T` and optionally AC‑i (§B) before storage or transmission.

**Commutation.** `send(T(H))` equals `T(send(H))` up to logs; `receive` handler runs `T` before CRDT to guarantee canonical forms and merge determinism.

**Budgets.** Compression budgets negotiated per channel; agents can request **lossless** resends for ambiguous queries.

---

## Page 11 — Trust, identity, and provenance

Agents maintain **trust graphs** `Trust : Agent×Agent→[0,1]` updated from track records and groundings.

**Policy hooks.**

* Trust‑weighted collapse.
* Quorum thresholds for strict upgrades.
* Reputation decay.

**Provenance.** Every edge records source agent IDs, timestamps, signatures, and hash of the supporting capsules.

---

## Page 12 — Planning & control loop

Agents operate in sense‑interpret‑plan‑act loops with **selectors** driving control.

Pseudocode (high level):

```
loop t:
  obs ← observe()
  e   ← encode(obs)
  H   ← T(H ⊗ e)
  q   ← next_query(goals, H)
  a   ← answer(q, H)
  plan← plan_update(goals, a)
  cmds← act(plan)
  msgs← dialogue(goals, H)
  send(msgs)
```

Planning may run on coarse layers first (§16), refine as needed.

---

## Page 13 — Learning in agents (policy + interpreter)

Agents learn:

* **Policies** `π_θ` (dialogue, collapse, query selection).
* **Interpreter params** within allowed ranges (e.g., thresholds, torsion dictionaries) via guarded updates (`anti` first).

Losses combine: calibration, grounding error, QA utility, safety penalties (zone leaks, unauthorized collapses). Updates respect **tower rule** and require down‑lift audits for persistent changes.

---

## Page 14 — Multi‑agent algorithms

**A. Distributed QA.** Route queries to agents with highest expected answer utility; aggregate credal answers with trust weights.

**B. Consensus by proof.** For critical facts, require `Proof Π` under protocol `Pr`; else remain tentative.

**C. Schema alignment.** Use AC‑5 sketches to propose alignments; verify with WL and DPO; adopt via `Propose/Agree` acts.

**D. Active grounding.** Select interventions that maximally reduce uncertainty across agents.

**E. Conflict mediation.** Run **alternative worlds** as zones `Z_alt` and compare utility before collapse.

---

## Page 15 — Worked examples

**W1: Two robots and a shelf.** A1 observes `on(box,shelf)`; A2 observes `near(box,shelf)`. Merge creates `⋈` capsule; grounding protocol with force sensor promotes `on` to strict; DPO adds `contact` and removes `near` edge in strict zone; paraphrase remains in source zones.

**W2: Dialogue QA.** A asks B: `where(on(cat,mat))?` B answers with capsule including detector version. A’s `Int` verifies, adopts edge tentatively; trust ↑ after repeated accuracy.

**W3: KB fusion.** Agents align schemas `on/atop`; `Propose` adds torsion rule; `Agree` after test suite passes; `T` ensures commutation; AC‑2 motifs compress stacks across agents.

---

## Page 16 — Metrics & evaluation

* **QA accuracy/latency** across agents.
* **Grounding ε** under distributed protocols.
* **Paraconsistent isolation**: leak rate of `⋈`.
* **Merge determinism** after `T`.
* **Compression ratio** vs selector utility.
* **Trust calibration** vs actual reliability.
* **Audit coverage**: share of messages with full capsules.

Benchmarks: blocks‑world multi‑robot, caption QA with multiple annotators, KG alignment corpora.

---

## Page 17 — Failure modes & guards

* **Version skew.** Different torsion dictionaries → divergence. Guard: negotiate versions; include dict hashes in capsules.
* **Malicious agents.** Signatures verify identity but not honesty; enforce protocol proofs for strict upgrades.
* **Flooding.** Rate‑limit and compress; drop lossy but keep strict capsule requests.
* **Zone contamination.** Disallow cross‑zone edge writes; quarantine offenders.
* **Interpreter drift.** Require `anti` previews and down‑lift audits.

---

## Page 18 — JSON APIs and capsules

**Dialogue act.**

```json
{
  "da": {
    "type": "Assert",
    "phi": "on(box#7,shelf#2)",
    "zone": "Z_src:A1",
    "sig": "ed25519:…",
    "time": "2025-09-18T12:00:00Z"
  }
}
```

**Evidence capsule.**

```json
{
  "capsule": {
    "sensor": "vision#A",
    "model": "surface-detector@1.3",
    "hash": "sha256:…",
    "protocol": "pr#42",
    "zone": "Z_src:A1",
    "attachments": ["…"],
    "signatures": ["…"]
  }
}
```

**Merge ack.**

```json
{
  "merge": {
    "anf_hash": "sha256:…",
    "crdt": {"vv": {"A1": 17, "A2": 9}},
    "dpo": [{"rule":"contact-required","applied": true}],
    "tension": {"capsules": 1}
  }
}
```

---

## Page 19 — Reference pseudocode

```pseudo
procedure HANDLE_MESSAGE(A, msg):
  msg ← T(msg)              // regen to ANF
  H   ← decode(msg)
  CRDT_MERGE(A.KG, H, zone=msg.zone)
  DPO_ENFORCE(A.KG, zone=msg.zone)
  if has_conflict(A.KG, zone): MARK_TENSION(A.KG, zone)
  if requires_reply(msg): out ← compose_reply(A, msg); send(out)
  LOG(A, msg)

procedure COMPOSE_REPLY(A, msg):
  match msg.type:
    case Ask(Q): return Answer(answer(Q, A.KG), capsule())
    case Propose(R): return Agree(R) if tests_pass(R) else Disagree(R)
    case Assert(φ): return Proof(Π) if can_ground(φ) else Ack

procedure TICK(A):
  obs ← observe(A.Cap)
  e   ← encode(obs); A.KG ← T(A.KG ⊗ e)
  msgs← dialogue(A); send_all(msgs)
  if meltdown(A): apply_guards(A)
```

---

## Page 20 — Next steps

1. Release a reference agent runtime with `Eff` handlers, CRDT+DPO merge, barrier policies, regen and compression.
2. Provide protocol language for grounding and dialogue acts with verifiers.
3. Publish multi‑agent benchmarks and audit harness.
4. Prove merge determinism under ANF and show confluence with DPO rules.
5. Extend to partial synchrony and adversarial settings; integrate trust learning with safety proofs.

---

*End of Appendix C — Agent‑Based Interpretation Framework (20pp v0.1).*


---

# MetaPrincipia Autopoietica — ADD‑ONS

## Appendix D — Aesthetic Constraints of **Living Logic** (Twenty‑Page Slab, v0.1)

> **Thesis.** Autopoietic semantics is not only true or useful; it is **shaped** by aesthetic constraints that bias systems toward compressible, symmetric, rhythmically stable structures. We formalize *aesthetic functionals* on scenes, proofs, interpreters, and dialogues; we show how these functionals couple to regen `T = R∘U`, paraconsistent zones `⋈`, and multi‑agent interaction; and we give algorithms, metrics, and tests.

**Dependencies.** Part I–IV; Appendix A (Regen), B (Compression), C (Agents).

**Page plan (20).**

1. Motivation and scope
2. Aesthetic substrate and invariants
3. Aesthetic primitives (symmetry, rhythm, proportion)
4. Functionals on scenes, proofs, and dialogues
5. Compatibility with regen and selectors
6. Symmetry groups on role‑hypergraphs
7. Rhythm and temporal form
8. Proportion and scale
9. Minimality, elegance, and MDL
10. Beauty–utility coupling
11. Paraconsistent poetics (tension aesthetics)
12. Agent aesthetics and conversational style
13. Algorithms for aesthetic scoring
14. Learning aesthetic priors
15. Metrics, audits, and user studies
16. Worked examples
17. Design guidelines and checklists
18. JSON schemas and APIs
19. Pseudocode and pipelines
20. Next steps

---

## Page 1 — Motivation and scope

Empirically, humans and effective systems favor **balanced** representations: symmetry, repetition with variation, proportional layering, and minimal description. In living logic, these become **regularizers** that bias regeneration, proof search, and dialogue toward **readable** and **maintainable** forms without sacrificing truth or safety.

We define aesthetics as objective functionals that are **computable** on aboutness hypergraphs and proof terms, with tunable weights and safety gates.

---

## Page 2 — Aesthetic substrate and invariants

Objects: scenes `H=|t|`, proof terms `π`, interpreter stacks `Int`, dialogues `D`.

Invariants:

* A1 **Truth‑compatibility**: aesthetics must not flip extensional truth.
* A2 **Selector coherence**: answers preserved within budgets.
* A3 **Regen commutation**: aesthetic pushes commute with `T` up to audit (§5).
* A4 **Paraconsistent safety**: aesthetics never collapse `⋈` without policy.
* A5 **Agent honesty**: stylistic changes preserve provenance and signatures.

---

## Page 3 — Aesthetic primitives

**Symmetry.** Group actions on roles and anchors; fixed‑point motifs; near‑symmetry with small defect sets.

**Rhythm.** Temporal repetition with phase offsets in dialogue or proof steps; cross‑scale beats via §16 scales.

**Proportion.** Ratios of subscene sizes and proof segment lengths; preferred bands (e.g., `[1.4, 1.8]`).

**Simplicity.** MDL/description length; node/edge density; torsion dictionary size.

**Contrast.** Alternation of tense/zone, agent roles, or operator families.

---

## Page 4 — Functionals on scenes, proofs, dialogues

We define an **aesthetic index** `𝔄` as a weighted sum of normalized scores:

```
𝔄(H,π,D) = w_sym S_sym(H) + w_rhy S_rhy(D) + w_prop S_prop(H) + w_mdl S_mdl(H,π)
            + w_con S_con(H,D) + w_smt S_smooth(Int) − w_ten C_tension(H)
```

with weights `w_* ≥ 0`. Each term is in `[0,1]`; `C_tension` penalizes unresolved `⋈` outside designated capsules.

**Goal.** Maximize `𝔄` subject to invariants A1–A5 and task utility.

---

## Page 5 — Compatibility with regen and selectors

**Theorem D.1 (Regen‑aesthetic commutation).** If a beautifier `B` preserves ANF boundaries and does not invent edges, then there is a natural iso `β: T∘B ⇒ B∘T` and selector answers are unchanged on the strict fragment.

*Sketch.* From Appendix A strong monoidality and selector naturality; `B` rearranges but does not alter role incidence.

---

## Page 6 — Symmetry groups on role‑hypergraphs

Let `G` act on anchors and roles by automorphisms. Define a **symmetry score**

```
S_sym(H) = max_{g∈G} 1 − d(H, g·H)
```

with `d` a role‑aware edit distance normalized to `[0,1]`. For **near‑symmetry**, discount by the fraction of moved elements.

**Group library.** Spatial (dihedral), causal (partial orders), role dualities (Agent↔Theme), and dialogue alternation (A↔B) groups.

---

## Page 7 — Rhythm and temporal form

Dialogue or proof sequences `σ = (s_1,…,s_n)` carry **beats** detected via autocorrelation of operator families and role changes. Define

```
S_rhy(D) = 1 − var(IBI) / var_ref
```

where `IBI` are inter‑beat intervals; `var_ref` is a baseline. Penalize **arrhythmia** (bursts without structure); reward **syncopation** (structured off‑beats) with a bounded bonus.

---

## Page 8 — Proportion and scale

For a partition of a scene into subscenes with sizes `(a,b)`, define proportion score

```
S_prop = exp( − ( log(a/b) − μ )^2 / (2σ^2) )
```

with `(μ,σ)` encoding a **preference band** (e.g., golden‑ish). Extend to multiscale by comparing layer sizes (§16) across scales; encourage geometric decay or growth patterns.

---

## Page 9 — Minimality, elegance, and MDL

Use **MDL** to penalize redundancy and reward concise codes:

```
S_mdl = 1 − min(1, L(H,π)/L_ref)
```

with `L` the combined description length (motif dictionary + pointers + proofs) and `L_ref` a baseline. Couple to AC‑2/3/4 compressors and proof normalization.

---

## Page 10 — Beauty–utility coupling

Define task utility `U` (QA, planning). **Coupled objective**

```
J = U − λ (1 − 𝔄)
```

Use `λ` schedule: start small, increase as competence stabilizes. Prove **no‑regret** bounds when beautifier steps are projections onto convex aesthetic sets; otherwise give empirical gates with anti‑previews and rollbacks.

---

## Page 11 — Paraconsistent poetics (tension aesthetics)

Not all `⋈` is ugly. Define capsule‑level **tension curvature** (density of minimal contradictions) and **resolution cadence** (time to collapse under policy). Reward:

* well‑isolated `⋈` with informative boundaries,
* balanced opposing motifs,
* timely resolution when evidence arrives.

Penalty for leaks or unresolved overload.

---

## Page 12 — Agent aesthetics and conversational style

Agents exchange scenes plus **style capsules**: preferred symmetry groups, rhythm bands, typography/serialization hints. Negotiation aligns to the **intersection** of preference sets. Trust interacts: agents that keep aesthetics stable gain higher acceptance in human‑in‑the‑loop.

**Style‑safe law.** Style transforms commute with `T` and do not alter strict facts.

---

## Page 13 — Algorithms for aesthetic scoring

**Inputs.** Scene `H`, proof `π`, dialogue `D`, interpreter `Int`.

**Steps.**

1. Compute ANF; extract motif multiset and layer sizes.
2. Estimate group action closeness for library `G`.
3. Detect beats in `D`/`π` via operator markers.
4. Compute MDL using AC‑2/3/4 summaries.
5. Combine into `𝔄` with calibrated weights.

**Complexity.** Near‑linear with precomputed motifs; group closeness uses WL fingerprints; rhythm detection is linear.

---

## Page 14 — Learning aesthetic priors

Train a scorer `𝒮_θ` on curated datasets (human‑rated proofs/dialogues/scenes) with **safety** constraints:

* Loss = α·ranking + β·calibration + γ·consistency under `T`.
* Adversarial: ensure no truth flips; detect bias; require counterfactual checks.
* Distill to light models for online scoring.

Use `𝒮_θ` to guide search (beam or MCTS) with an **aesthetic bonus**; gate by `anti` and replay.

---

## Page 15 — Metrics, audits, and user studies

**Metrics.** `𝔄` distributions, inter‑rater correlation, selector preservation, time‑to‑comprehension, error rates under edits.

**Audits.** Randomized **AB** on beautified vs raw outputs; compute regression on task outcomes. Track leaks across `⋈` and any changes to strict zones.

**User studies.** Proof readability, dialogue clarity, and scene diagram legibility.

---

## Page 16 — Worked examples

**E1 (Scene symmetry).** Stack of `on` relations compressed to a motif; apply role duality symmetry; answers preserved and `𝔄↑`.

**E2 (Proof rhythm).** Sequent proof with repeated `∀`‑intro beats; beautifier groups steps; no change in theorems; `𝔄↑`.

**E3 (Dialogue proportion).** QA exchange refactored to question→answer→evidence cadence with proportional segment lengths; faster comprehension; no semantic change.

---

## Page 17 — Design guidelines and checklists

* Prefer ANF then beautify.
* Keep symmetry groups explicit; document near‑symmetries.
* Maintain rhythmic cadences in tutorials and agent prompts.
* Check MDL before shipping; avoid over‑compression.
* Preserve `⋈` capsules; never collapse by style.
* Log style transforms and hashes.

**Checklist.** Truth unchanged; selectors stable; regen commute; zones intact; signatures intact; audits green.

---

## Page 18 — JSON schemas and APIs

**Aesthetic report.**

```json
{
  "aesthetic": {
    "sym": 0.72,
    "rhy": 0.63,
    "prop": 0.58,
    "mdl": 0.81,
    "con": 0.55,
    "tension_pen": 0.04,
    "A": 0.71,
    "commutes_with_T": true,
    "notes": "dihedral~0.8; golden-band μ=0.47"
  }
}
```

**Preference capsule.**

```json
{
  "style": {
    "groups": ["D4","AgentThemeDual"],
    "rhythm": {"target_bpm": 90, "syncopation": 0.2},
    "proportion": {"mu": 0.47, "sigma": 0.18},
    "strict": true
  }
}
```

---

## Page 19 — Pseudocode and pipelines

```pseudo
function BEAUTIFY(H, π, D, prefs):
  H ← T(H)                     // regen to ANF
  S_sym ← SYMMETRY_SCORE(H, prefs.groups)
  S_rhy ← RHYTHM_SCORE(D, π, prefs.rhythm)
  S_prop← PROPORTION_SCORE(H, prefs.proportion)
  S_mdl ← MDL_SCORE(H, π)
  A    ← COMBINE(S_sym,S_rhy,S_prop,S_mdl, prefs.weights)
  if A↑ and invariants_hold():
    return APPLY_STYLE_TRANSFORMS(H,π,D,prefs), A
  else:
    return (H,π,D), A
```

**Guard rails.** Every transform runs under `anti`; strict zones immutable; emit audit capsule with before/after hashes.

---

## Page 20 — Next steps

1. Release a reference aesthetic scorer and beautifier with proofs of regen commutation.
2. Publish symmetry libraries and rhythm detectors.
3. Run user studies and AB tests; tune weights.
4. Integrate with agent framework; expose preference negotiation.
5. Extend to visualization and typographic rendering guidelines.

---

*End of Appendix D — Aesthetic Constraints of Living Logic (20pp v0.1).*


---


# MetaPrincipia Autopoietica — ADD‑ONS

## Appendix E — Role Lexicons and Semantic Torsion Maps (Twenty‑Page Slab, v0.1)

> **Objective.** Specify **role lexicons** and **semantic torsion maps** that operationalize prepositions/relators as typed, topological operators across languages and domains, with executable guards, learning procedures, and safety. Deliver lossless ANF compatibility with regen `T = R∘U`, selector coherence, and paraconsistent isolation.

**Prereqs.** Part I (symbol system), Part II §5–§8 (aboutness, axioms, barriers, regen), Part III §9–§12 (language, KGs, agents), Part IV §13–§16 (grounding, meta‑interpretation, emergence, autopoiesis). Appendix A–D.

**Page plan (20).**

1. Scope and primitives
2. Role taxonomy and kinding
3. Core relator signatures
4. Extended domain roles
5. Lexicon entry schema
6. Torsion maps: definition
7. Equivalence, inclusion, substitution
8. Topological semantics
9. Cross‑lingual mapping
10. Disambiguation algorithms
11. Learning from data
12. Regen commutation
13. Paraconsistent handling
14. Selector coherence
15. Metrics and audits
16. Worked spatial set
17. Domain adapters
18. APIs and capsules
19. Pseudocode and pipelines
20. Next steps

---

## Page 1 — Scope and primitives

A **role lexicon** `Lex` assigns to each *relator form* `f` one or more **typed relators** `R` with signatures, guards, and topology. A **torsion map** `τ` specifies controlled transformations among relators/forms that preserve **aboutness** up to guarded isomorphism.

**Objects.**

* `Rel` (typed relators), `Role` (Agent, Theme,…), `Guard` (predicates), `Topo` (orientation/attachment), `Lang` (language code), `Zone` (paraconsistent locality), `Capsule` (provenance).

**Invariants.**

* ANF compatibility (Appendix A), selector coherence (Part III §9), paraconsistent isolation (Part II §7), tower safety (no down‑lifts invented).

---

## Page 2 — Role taxonomy and kinding

**Canonical roles.** `Agent, Theme, Experiencer, Stimulus, Instrument, Source, Goal, Path, Location, Region, Surface, Container, Containment, Time, Manner, Cause, Purpose, Beneficiary, CoTheme`.

**Kinds.** `Role : 𝒰₀`, `Rel : Role^k → Prop`, `Guard : Thing^m → Bool`, `Topo : record{orient, attach, nest, metric?}`.

**Role partial order.** Some roles refine others, e.g., `Surface ⊑ Location`, `Container ⊑ Region`. Lexicon constraints may **require** a refinement (e.g., `on` requires `Surface(y)`).

---

## Page 3 — Core relator signatures

Spatial core (binary unless stated):

```
IN      : (Theme, Container) → Prop         guard: Container(y)
ON      : (Theme, Surface) → Prop           guard: Surface(y), Contact(x,y)
AT      : (Theme, Location) → Prop          guard: Location(y)
OVER    : (Theme, Reference) → Prop         guard: Altitude(x) > Altitude(y)
UNDER   : (Theme, Reference) → Prop         guard: Altitude(x) < Altitude(y)
THROUGH : (Theme, Region|Medium) × Path?    guard: Permeable(y), Path(x,y)
ACROSS  : (Theme, Region) → Prop            guard: Span(x,y)
BETWEEN : (Theme, Reference×Reference)      guard: Betweenness(x;y1,y2)
AROUND  : (Theme, Reference) → Prop         guard: Encircles(x,y)
NEAR    : (Theme, Reference) → Prop         guard: dist(x,y) < θ
```

Causal/instrumental:

```
BY(inst) : (Agent/Process, Instrument) → Prop  guard: Enables(i,x)
WITH     : (Agent/Theme, CoTheme|Instrument)   guard: CoPresent(x,y) ∨ Enables(y,x)
FROM     : (Theme, Source) → Prop              guard: Source(y)
TO       : (Theme, Goal) → Prop                guard: Goal(y)
```

Each signature includes **topology** (orientation, attachment sites) and **evaluation order** (which arguments must be grounded first).

---

## Page 4 — Extended domain roles

Add domain‑specific refinements:

* **Robotics:** `GraspSite ⊑ Surface`, `Workspace ⊑ Region`, `Obstacle ⊑ Reference`.
* **Biomed:** `AnatomicalRegion ⊑ Region`, `Carrier ⊑ Medium`, `Dose ⊑ Instrument`.
* **Legal:** `Party ⊑ Agent`, `Contract ⊑ Reference`, `Jurisdiction ⊑ Region`.
* **Data:** `Table ⊑ Container`, `Column ⊑ Region`, `Index ⊑ Path`.
  Each adapter ships **guard libraries** and **measurement protocols** (§13; Part IV §13).

---

## Page 5 — Lexicon entry schema

**Conceptual record.**

```
LexEntry = {
  id, lang, form, relator, arity, roles:[RoleSpec],
  topo: {orient, attach, nest, metric?},
  guards: [GuardSpec],
  semantics: {extensional, intensional},
  selectors: {answerable: [who, where, …]},
  provenance: Capsule, version, tests
}
```

**JSON.**

```json
{
  "id": "en:on.surface.v1",
  "lang": "en",
  "form": "on",
  "relator": "ON",
  "arity": 2,
  "roles": [
    {"name": "Theme", "type": "Thing"},
    {"name": "Surface", "type": "Thing"}
  ],
  "topo": {"orient": "contact+support", "attach": ["Theme","Surface"], "nest": false},
  "guards": ["Surface(y)", "Contact(x,y)"]
}
```

Entries admit multiple **senses** keyed by guards.

---

## Page 6 — Torsion maps: definition

A **torsion map** `τ` is a partial, guard‑indexed transformation among relators/forms preserving aboutness up to a **role‑preserving isomorphism**.

**Definition (role‑preserving iso).** A bijection `ϕ_V:V→V′` on anchors and a family of bijections `ϕ_E` on hyperedges such that for each edge `e` with role incidence `ι_e : Role→V`, there exists `e′` with `ι_{e′} = ϕ_V ∘ ι_e ∘ π` where `π` is a **role permutation constrained by the torsion**, typically identity.

**Examples.**

* `τ(on → atop)` under `Surface(y)` and `Contact(x,y)`.
* `τ(near ↔ within δ)` with metric guard.
* Cross‑lingual `τ(fr:sur ↔ en:on)` with sense guard.

**Functor view.** Torsions are natural transformations between functors `Lex_lang → RelCat`.

---

## Page 7 — Equivalence, inclusion, substitution

**Equivalence (≈\_τ).** `R ≈_τ R′` iff there exists `τ` bidirectional with guards `g, g′` s.t. `g∧g′` satisfiable and `R`/`R′` realize to isomorphic edges under `ϕ`.

**Inclusion (⊑\_τ).** `R ⊑_τ R′` if `R` refines `R′` (stronger guards, stricter roles) and there is a one‑way torsion.

**Substitution law.** If `R ⊑_τ R′` and query `q` is **insensitive** to differences outside τ’s guards, then `q(R(x,y))` equals `q(R′(x,y))`. Sensitivity catalog is part of selectors metadata.

---

## Page 8 — Topological semantics

Relators embed **topology**:

* `IN` is **nested containment**: induces a partial order and supports **sheaf gluing** (§F).
* `ON` is **contact+support**: requires `Surface`, yields `contact(x,y)`.
* `THROUGH` is **path in medium**: parameterized by path; composes with `ACROSS` if alignment holds.
* `OVER/UNDER` order altitude; define continuous variants with metrics.

Torsions must respect topological invariants, e.g., `on→over` only if contact is optional and altitude remains `>`. Guards enforce this.

---

## Page 9 — Cross‑lingual mapping

**Lex layers.** `Lex_lang` maps surface forms to relators with guards. Build a **pivot lexicon** `Lex*` of abstract relators; compile per language:

```
compile_lang(lang) : Lex* → Lex_lang
```

**Torsion bundles.** For each pair `(lang₁, lang₂)`, pack torsions `τ_{lang₁→lang₂}` with guards and tests. Example:

* `fr:sur ↔ en:on.surface`
* `ja:ni (locative)` splits into `{AT, IN}` by guards.

**Disambiguation** uses role/context features (Page 10).

---

## Page 10 — Disambiguation algorithms

**Task.** Map a token/form to a typed relator sense.

**Inputs.** Context embeddings, detected anchors, candidate roles, guards (soft/firm), topology hints.

**Algorithm (hybrid).**

1. Generate candidates by lexicon `Lex_lang(form)`.
2. Score guards with detectors (`Surface`, `Container`, `Path`).
3. Run **topo‑consistency** solver to prune impossible senses.
4. Use a small **role‑equivariant** classifier to rank remaining.
5. Apply torsion preferences from domain adapter; pick top or return **credal set** if scores close.

**Complexity.** Linear in senses; detector cost dominates.

---

## Page 11 — Learning from data

**Sources.** Parallel text, captioned scenes, robotics telemetry, KB triples with spatial tags.

**Learnable elements.** Guard thresholds, detector params, torsion probabilities, role priors.

**Procedure.**

* Weakly supervise guards from intervention logs (contact sensors, containment checks).
* EM over latent senses with ANF constraints.
* Calibrate with **selector regression**: answers must match gold QA after mapping.

**Safety.** Learning never edits strict zones or down‑lifts; all proposals pass through `anti` preview with audits.

---

## Page 12 — Regen commutation

**Theorem E.1 (Lex‑regen commutation).** If lexicon entries obey ANF boundaries and torsion maps are recorded as code facts, then

```
T ∘ map_lex ≅ map_lex ∘ T
```

for mapping operations `map_lex` that insert relator edges and labels.

*Sketch.* From Appendix A strong monoidality and selector naturality; mapping is structural and zone‑local.

---

## Page 13 — Paraconsistent handling

Conflicting senses from multiple sources form `⋈` capsules:

* Keep per‑source zones `Z_src:i`.
* Do **not** unify unless a collapse policy triggers (proof, majority with trust, grounding protocol).

Selectors return **credal** answers with capsule citations. Torsion maps **never** cross zones implicitly.

---

## Page 14 — Selector coherence

**Claim.** Selector `where(ON(x,y))` equals `where(ATOP(x,y))` under `τ(on→atop)` guards. Provide **selector sensitivity lists** in `LexEntry` indicating invariances.

**Proof idea.** Aboutness is invariant under role‑preserving iso; selectors are functions of aboutness projections.

---

## Page 15 — Metrics and audits

**Quality metrics.**

* **Guard accuracy** (ECE, precision/recall).
* **Selector stability** before/after torsion.
* **Cross‑lingual consistency** on parallel datasets.
* **ANF commutation** violations (should be zero).
* **Paraconsistent leak** rate across zones.
* **Coverage** of domain adapters.

**Audits.** Randomized spot checks with regen certificates (Appendix A), selector regression suites, guard challenge sets.

---

## Page 16 — Worked spatial set

**English spatial micro‑lexicon.**

```
EN.ON.surface: roles(Theme,Surface), guards[Surface(y),Contact(x,y)], topo(contact+support)
EN.ON.top:     roles(Theme,Surface), guards[Surface(y),Above(x,y)], topo(no-contact)
EN.IN.container: roles(Theme,Container), guards[Container(y)], topo(nested)
EN.OVER.ref:   roles(Theme,Reference), guards[Altitude(x)>Altitude(y)], topo(order)
EN.THROUGH.medium: roles(Theme,Medium), guards[Permeable(y),Path(x,y)]
EN.ACROSS.region:  roles(Theme,Region), guards[Span(x,y)]
```

**Torsions.**

```
τ1: ON.surface → ATOP  if Contact(x,y) ∧ Surface(y)
τ2: OVER.ref → ABOVE   if NoPath(x,y) ∧ ¬Contact(x,y)
τ3: THROUGH.medium ↔ ACROSS.region  if Alignment(path,span) ∧ Permeable(y)
```

Selectors unchanged under τ1; partially sensitive under τ2/τ3 with documented exceptions.

---

## Page 17 — Domain adapters

**Robotics adapter (RB‑v1).**

* Guards implemented by detectors: `Surface(y)` via plane fit; `Contact(x,y)` via force/torque; `Path(x,y)` via planner logs.
* Torsion priors favor `ON.surface` when contact≥τ\_c.

**Biomed adapter (BM‑v1).**

* `IN` maps to **anatomical containment**; `WITH` as **co‑administration**; `BY` as **mechanism**.
* Guards rely on ontology tags; torsion between `IN` and `AT` depends on region type.

**Legal adapter (LG‑v1).**

* `BY(Agent, Instrument)` → *by means of* clause; `WITH` often **comitative**; `IN` as **jurisdiction**.

---

## Page 18 — APIs and capsules

**Lexicon API.**

```json
{
  "lex.lookup": {"form": "on", "lang": "en", "context": "…"},
  "lex.resolve": {"candidates": ["en:on.surface.v1","en:on.top.v1"], "scores": [0.71,0.29]},
  "lex.torsion": {"from": "EN.ON.surface", "to": "EN.ATOP", "guards": ["Surface(y)","Contact(x,y)"]}
}
```

**Capsule.**

```json
{
  "lexCapsule": {
    "entry": "en:on.surface.v1",
    "guards": {"Surface": 0.93, "Contact": 0.88},
    "provenance": {"source": "detector@1.4", "time": "2025-09-18"},
    "zone": "Z_src:cam1",
    "sign": "ed25519:…"
  }
}
```

---

## Page 19 — Pseudocode and pipelines

```pseudo
function MAP_RELATOR(token, anchors, ctx, lang):
  C ← CANDIDATES = Lex[lang].lookup(token)
  for c in C:
    c.score ← GUARD_SCORE(c.guards, anchors, ctx) + TOPO_SCORE(c.topo, anchors)
  C ← FILTER_TOPO_INCONSISTENT(C)
  if CONFUSION(C) high: return CREDAL_SET(C)
  best ← argmax(C.score)
  return best

function APPLY_TORSION(edge, τ):
  if CHECK_GUARDS(τ.guards, edge):
    return TRANSFORM(edge, τ)
  else: return edge

pipeline LEXICALIZE(scene, lang):
  for token in scene.tokens:
    entry ← MAP_RELATOR(token,…)
    scene ← INSERT_EDGE(entry.rel, entry.roles,…)
  return T(scene)  // regen to ANF
```

**Complexity.** Linear in tokens with small candidate sets; guard scoring dominates.

---

## Page 20 — Next steps

1. Publish **Core‑30** role lexicon with tests and torsion maps for EN/FR/ES/JA.
2. Release **RB‑v1** and **BM‑v1** adapters with guard detectors and evaluation scripts.
3. Ship disambiguation models and selector regression harness.
4. Integrate lexicon API into the agent framework (Appendix C) and regen (Appendix A).
5. Extend torsion functors to compositional schemas and continuous spatiotemporal fields.

---

*End of Appendix E — Role Lexicons and Semantic Torsion Maps (20pp v0.1).*
