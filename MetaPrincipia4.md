# MetaPrincipia Autopoiētica — Part IV: Metasemantic Foundations

## §13. Grounding: Mind • World • Model — Interpretive Stance, Situational Realism, Symbolic Realism (Twenty‑Page Slab, v0.1)

> **Thesis.** Meaning is *grounded* when symbols stably co‑vary with situation structure under specified interventions. We formalize a tripos ⟨Mind, World, Model⟩ with stance‑indexed interfaces, give **situational realism** (world as structured situations) and **symbolic realism** (symbols as faithful functors into situation structure), and provide algorithms, proofs, and protocols that bind our calculus 𝒞\_A to actual measurement.

**Standing context.** Part I (symbols, kinds), Part II §5–§8 (aboutness, recursive axioms, barriers, regen `T`), Part III §9–§12 (language, mathematics, reflexivity, agents & KGs).

**Page plan (20):**

1. Goal & scope
2. Ontology: Mind/World/Model tripos
3. Stances: agent‑centric, environment‑centric, intersubjective
4. Situational realism (SIT)
5. Symbolic realism (SYM)
6. Interfaces and channels (observe/act/declare)
7. Grounding diagrams and commutative squares
8. Extensional, intensional, aboutness grounding
9. Causal grounding with SCMs
10. Measurement protocols & instrumentation
11. Calibration, identifiability, sufficiency
12. Regen‑assisted grounding (T = R∘U)
13. Barrier‑aware grounding in paraconsistent data
14. Algorithms: learn‑to‑ground
15. Worked examples I (toy worlds)
16. Worked examples II (language & perception)
17. Benchmarks & metrics
18. Failure modes & guards
19. JSON export schemas
20. Next‑step plan

---

## Page 1 — Goal & scope

We give a **formal contract** that tells when a representation in 𝒞\_A counts as grounded. The contract is testable: it specifies interventions, observables, and acceptance criteria. The result ties aboutness hypergraphs to measurable reality while respecting meta‑coherence (barriers, zones).

---

## Page 2 — Ontology: Mind/World/Model tripos

Let:

* **World `W`**: a category of situations `SIT` with objects `s∈S` and morphisms `ι:s→s′` (inclusions, time steps, controlled interventions).
* **Mind `MIND`**: agent‑internal states `Σ` with policies `Pol` and knowledge graph `KG` (§12).
* **Model `MOD`**: a 𝒞\_A term space with meanings `S(t)=(⟦t⟧_E,⟦t⟧_I,|t|)` and rewrite ℛ\_A.

Channels:

* Observation `obs : S → Obs`.
* Actuation `act : Cmd → S×S`.
* Declaration `decl : MOD → Msg`.

The **grounding problem** is to synthesize `Γ : Obs → MOD` and `Ξ : MOD → Exper` such that induced predictions align with `W` under interventions.

---

## Page 3 — Stances: agent‑centric, environment‑centric, intersubjective

A **stance** parameter `σ` configures the contract:

* **Agent‑centric**: ground to *this* agent’s sensors/acts; permits subjectivity; compares across time.
* **Environment‑centric**: ground to instrumented world channels; aims at inter‑agent agreement via shared protocols.
* **Intersubjective**: ground to a committee of agents via consensus and CRDT (§12).

Grounding judgments carry `σ` as an index: `⊢_σ ground(t ↔ Φ)` where `Φ` is a situation predicate.

---

## Page 4 — Situational realism (SIT)

**Definition (situational base).** A *situation structure* is ⟨`S, ℛ_s, Att`⟩ where `S` is a set of anchors (objects, regions, times), `ℛ_s` a set of typed relations with roles, and `Att` attributes. A **world** `W` is a presheaf `Sit : 𝒥^op→Set` over a site `𝒥` of observation contexts; restriction maps encode partiality.

Truth is **situational**: a proposition `φ` is true *in* situation `u∈Ob(𝒥)` iff `⟦φ⟧(u)=1`. Interventions change arrows in `𝒥` and/or values of `Att`.

---

## Page 5 — Symbolic realism (SYM)

**Definition (symbolic realism).** There exists a **faithful functor**

```
J : Hyp → Str(SIT)
```

from aboutness hypergraphs to structured situations such that:

1. Role preservation: roles/relators map to relation symbols with the same incidence.
2. Limit/colimit preservation on a declared fragment (pullbacks for substitution; pushouts for gluing).
3. Measurement compatibility: each primitive predicate has a measurement method in `SIT` with specified error model.

Faithfulness means distinct hypergraph edges don’t collapse under `J` unless torsion dictionary `D*` says so.

---

## Page 6 — Interfaces and channels (observe/act/declare)

Interfaces are **typed** and **audited**:

```
observe_π : SIT → Obs         // policy‑parameterized sensing
encode   : Obs → MOD          // Γ
predict  : MOD → Pred(SIT)    // Ξ; predicted situation properties
execute  : Cmd → SIT×SIT      // actuation
```

All are zone‑aware. `observe` may output `⋈` when sensors disagree; `encode` must preserve uncertainty as zones or weights.

---

## Page 7 — Grounding diagrams and commutative squares

A representation `t∈MOD` is *ε‑grounded* to a situation predicate `Φ` if the following square **ε‑commutes** under a policy π and test distribution D:

```
      SIT  ──observe_π──▶  Obs  ──encode──▶  MOD
       │                         │            │
       │ Φ (measurement)         │ ⟦t⟧        │ Ξ
       ▼                         ▼            ▼
   Truth values              Pred(SIT)   ──compare_π──▶  {ok,err}
```

We require `err ≤ ε` under interventions drawn from a family `𝕀`.

---

## Page 8 — Extensional, intensional, aboutness grounding

Grounding decomposes across the tri‑layer:

* **Extensional**: `⟦t⟧_E` matches measured truth across `𝕀`.
* **Intensional**: `⟦t⟧_I` maintains world‑indexed profiles consistent under accessibility relations (modality tests).
* **Aboutness**: `|t|` aligns with `J^{-1}` of measured situation relations; evaluate via graph kernels and incidence checks.

**Theorem (Tri‑homomorphism).** If `encode` and `Ξ` are homomorphisms w\.r.t. syntactic composition, then grounding on primitives extends to composites with bounded error accumulation.

---

## Page 9 — Causal grounding with SCMs

Let `M = (U,V,F,P(U))` be a **structural causal model** over situations. A symbol `t` is **causally grounded** in `M` if interventions on parents of the target predicate produce predicted changes in `⟦t⟧` matching `do(·)` effects.

**Criterion.** For `Φ=Φ(V)`,

```
Ξ(t | do(X←x)) ≈ P(Φ=1 | do(X←x))
```

across a test set. For aboutness, edges in `|t|` must align with the Markov blanket of Φ.

---

## Page 10 — Measurement protocols & instrumentation

Define **measurement specs** `μ`:

```
μ ::= ⟨target Φ, sensor s, procedure P, error ε, calibration κ⟩
```

A **protocol** `Pr` is a sequence of specs with preconditions and intervention scripts. Logs are first‑class; every grounding judgment cites the executed `Pr` and its capsules (§19).

**Repeatability.** Grounding requires inter‑run stability under the same `Pr` up to ε.

---

## Page 11 — Calibration, identifiability, sufficiency

* **Calibration**: predicted probabilities vs empirical frequencies; score with ECE/Brier.
* **Identifiability**: parameters of `Ξ∘encode` are uniquely determined from `Pr`; else report equivalence classes.
* **Sufficiency**: embeddings/latents derived by `U` must be **statistically sufficient** for the measured predicates; use mutual‑information lower bounds under constraints.

**Lemma (Minimal sufficient grounding).** If `U` is an information bottleneck retaining all information about Φ given sensors, then `R∘U` is the minimal canonicalizer achieving the same calibration.

---

## Page 12 — Regen‑assisted grounding (T = R∘U)

Use `T` to canonicalize before comparison. `U` extracts codes `(roles, anchors, torsion)`; `R` rebuilds ANF. Gaps from `Δ(U s)` (missing roles, ambiguity) become **grounding tasks**: request sensors, spawn placeholders, or split zones. Convergence is monitored by a **budget** that decays when no new evidence arrives (§8).

---

## Page 13 — Barrier‑aware grounding in paraconsistent data

Sensors disagree → mark edges with `⋈` in a *sensor zone*. Queries default to **credal** mode (interval answers). Collapse occurs only under explicit policy (authority/recency/minimal‑change). **Local Non‑Explosion** ensures unrelated parts of the KG remain valid (§7).

**Rule.** Grounding cannot be declared **strict** if supporting evidence lives in a `⋈` zone.

---

## Page 14 — Algorithms: learn‑to‑ground

Pipeline:

1. Collect sensor streams and interventions `𝕀`.
2. Build situation traces; execute `observe_π`.
3. `encode` to 𝒞\_A; run `T`; attach provenance capsules.
4. Train `Ξ` to map 𝒞\_A terms to predicted situation properties with losses:

```
L = L_ext + λ_I L_int + λ_A L_about + λ_cal L_cal + λ_cau L_causal
```

5. Validate under held‑out interventions; audit errors.

Optimization: alternating EM‑style updates on `encode` (structure) and `Ξ` (parameters).

---

## Page 15 — Worked examples I (toy worlds)

**Gridworld colors.** `Φ = “cell (i,j) is red”`. Sensors noisy; `encode` builds anchors for cells; aboutness edges for adjacency. Causal test: repaint via `do(color←blue)`; grounded symbol must flip truth accordingly; calibration checked.

**Blocks world spatial** (`on, in, left_of`). Interventions: move blocks; measured relations update. `J` maps `|t|` into contact/containment; torsion dictionary equates `on/atop`.

---

## Page 16 — Worked examples II (language & perception)

**Caption grounding.** Text “the cat on the mat” → `on(Cat,Mat)`. Vision protocol extracts surfaces via a learned `Surface(y)` detector; grounding holds if contact is measured within tolerance. Questions `where(…)` read off aboutness anchors.

**Dialogic grounding.** Two agents assert conflicting locations; edges stored in separate zones with `⋈`. Strict answers suspended; credal answers returned until policy collapse with evidence.

---

## Page 17 — Benchmarks & metrics

* **Grounding accuracy** under interventions.
* **Causal faithfulness**: counterfactual parity gap.
* **Aboutness fidelity**: WL‑kernel between `|t|` and `J^{-1}` of measured scenes.
* **Calibration**: ECE/Brier/LL.
* **Stability** across runs of `Pr`.
* **Paraconsistent isolation**: leak rate from `⋈` zones.
* **Budget efficiency**: edits per accepted grounding.

---

## Page 18 — Failure modes & guards

* **Symbol drift**: `encode` changes mapping without log; guard with hash‑anchored torsion dictionaries and diffs.
* **Spurious correlations**: extensional fit without causal validity; require `L_cau`.
* **Zone leakage**: evidence crosses barriers; enforce per‑zone evaluation.
* **Over‑collapse**: premature policy decisions; use counterfactual store and rollback.
* **Under‑specification**: insufficient protocol; report non‑identifiability with concrete missing interventions.

---

## Page 19 — JSON export schemas

**Grounding capsule.**

```json
{
  "term": "on(cat#1,mat#1)",
  "stance": "environment",
  "protocol_id": "pr#42",
  "interventions": ["move(cat#1,mat#1)", "lift(cat#1)"] ,
  "evidence": [{"sensor":"vision#A","time":"...","hash":"sha256:...","zone":"Z_sense"}],
  "aboutness_fidelity": 0.97,
  "causal_faithfulness": 0.93,
  "ece": 0.02,
  "strict": true,
  "notes": "tolerances 2cm; surface detector v1.3"
}
```

**Measurement spec.**

```json
{
  "id":"pr#42",
  "target":"on(x,y)",
  "sensors":["vision#A","force#B"],
  "procedure":"place x on y; record contact map; repeat n=10",
  "error_model":"Gaussian σ=0.5cm",
  "interventions":["do(position(x)=...)"],
  "acceptance":{"epsilon":0.05,"trials":10}
}
```

---

## Page 20 — Next‑step plan

1. Implement stance‑indexed grounding checks with SCM hooks and per‑zone isolation.
2. Release protocol language and auditor for capsules/logs.
3. Integrate with §9 selectors, §12 dialogue APIs, and §8 regen budgets for active data collection.
4. Provide reference tasks (gridworld, blocks, captioning) with intervention scripts and evaluation code.

---

*End of Part IV §13: Grounding — Mind • World • Model (20pp v0.1).*


---


# MetaPrincipia Autopoietica — Part IV: Metasemantic Foundations

## §14. Meta‑Interpretation as Dynamical Frame — The Interpreter as a Recursive Effect; Meta‑Relators on Interpretation Functions (Twenty‑Page Slab, v0.1)

> **Thesis.** Interpretation is not a static mapping but a **dynamical frame** that evolves with use. The interpreter itself is an **effect** whose behavior composes, can be transformed by meta‑relators, and admits fixed points under guards. We axiomatize interpretation as an *indexed effect algebra* with handlers, give operational and denotational accounts, and prove meta‑coherence with barriers and the regen monad `T = R∘U`.

**Prereqs.** Part I (symbols, kinds), Part II §5–§8 (aboutness, recursive axioms, barriers, regen), Part III §9–§12 (language, mathematics, reflexivity), Part IV §13 (grounding).

**Page map (20).**

1. Problem setup and motivation
2. Dynamical frames: objects and morphisms
3. Interpreters as effects
4. Algebraic operations and handlers
5. The interpreter category `Int`
6. Meta‑relators on interpreters
7. Stacked interpretation and towers
8. Operational SOS with effect rows
9. Denotational model (Eilenberg–Moore)
10. Grounded dynamic frames
11. Fixed points of interpretation (guarded Y)
12. Confluence, stability, and safety
13. Interaction with regen `T=R∘U`
14. Paraconsistent zones and handler barriers
15. Algorithms and complexity
16. Worked examples I (language)
17. Worked examples II (self‑modifying agents)
18. Diagnostics and metrics
19. JSON exports and APIs
20. Next steps

---

## Page 1 — Problem setup and motivation

Classical semantics fixes `⟦·⟧` once and for all. Autopoietic systems **reconfigure** interpretation through learning, policy changes, and interaction. We require a semantics where:

* the interpreter `𝕀` carries **state** and **policies**;
* composition of interpreters is typed and lawful;
* meta‑operations (questioning, inversion, parameterization) act **on interpreters**;
* fixed points exist but are **guarded** to avoid collapse.

---

## Page 2 — Dynamical frames: objects and morphisms

A **dynamical frame** is a tuple

```
F = ⟨State, Obs, Act, Pol, Upd, Out⟩
```

where `Upd : State × Act → State` and `Out : State × Obs → Val`.
Interpretation runs **in** a frame: meanings depend on `State` and may update it.

Morphisms between frames are structure‑preserving maps `f : F→F′` carrying states and operations forward and satisfying:

```
f_State ∘ Upd  = Upd′ ∘ (f_State × f_Act)
Out′ ∘ (f_State × f_Obs) = f_Val ∘ Out
```

Frames form a category `Dyn`.

---

## Page 3 — Interpreters as effects

Let `Expr` be well‑typed expressions of 𝒞\_A. An **interpreter** is an *algebraic effect*:

```
𝕀 : Expr → Eff Val
```

with `Eff` a monad capturing state, provenance, and tension:

```
Eff X ≔ State → (X × State × Log × Tension)
```

We write computations with effect rows `ρ` (e.g., `{state, prov, ⋈, policy}`) and use handlers to discharge them.

**Typing.** `Γ ⊢ e:τ  ⇒  Γ ⊢ 𝕀[e] : Eff_ρ τ`.

---

## Page 4 — Algebraic operations and handlers

We expose primitive **operations** used by interpretation:

```
get     : Eff State
put     : State → Eff 1
prov    : Capsule → Eff 1
mark⋈   : Edge → Eff 1
policy  : Query → Eff Answer
ask     : Selector×Prop → Eff Answers
regen   : Scene → Eff Scene        // calls T = R∘U
```

A **handler** `⟦·⟧^H : Eff_ρ τ → Eff_ρ′ τ` interprets or routes these ops. Handlers can be layered to assemble a full interpreter.

**Law.** Handlers compose associatively up to natural isomorphism; neutral handler acts as identity.

---

## Page 5 — The interpreter category `Int`

Objects: effectful interpreters `𝕀 : Expr→Eff_ρ Val` with fixed effect signature `ρ`.

Morphisms: **transformers** `τ : 𝕀⇒𝕀′` are natural transformations commuting with syntax constructors and preserving aboutness (cf. §5):

```
τ_e : 𝕀[e] ⇒ 𝕀′[e]    such that  |out(𝕀[e])| ≈̇ |out(𝕀′[e])|
```

Composition is vertical composition of natural transformations. With pointwise monoidal structure from handler stacking, `Int` is monoidal.

---

## Page 6 — Meta‑relators on interpreters

We lift meta‑relators to **endofunctors on `Int`**.

* `meta‑of(𝕀)` exposes an *inspector* interface: treats relations as objects during interpretation; adds op `inspect : Rel→Eff RelObj`.
* `anti⟨𝕀⟩` executes `𝕀` within a non‑committing barrier; state updates suppressed; only out values and logs produced.
* `trans(𝕀)` flips certain role orientations in outputs (e.g., input/output dual) according to a torsion dictionary.
* `para‑through(𝕀₁,𝕀₂)` pipes outputs of `𝕀₁` into `𝕀₂` at relator boundaries; coherent if handler interfaces match.

**Coherence.** When defined, `meta‑of` is a **strong monoidal functor**: `meta‑of(𝕀₁ ⊗ 𝕀₂) ≅ meta‑of(𝕀₁) ⊗ meta‑of(𝕀₂)`.

---

## Page 7 — Stacked interpretation and towers

Interpretation levels `ℓ = 0,1,2,…` with tower rule (§7): a level‑`ℓ` interpreter may *inspect* level `ℓ−1` artifacts; to **modify** them it must pass through an explicit **down‑lift** `↓` with audit.

```
𝕀@ℓ : Expr@ℓ → Eff@ℓ Val@ℓ
meta‑of(𝕀@ℓ) : Expr@ℓ → Eff@ℓ (Val@ℓ × Artifacts@ℓ)
```

Cross‑level functor `Lift : Int@ℓ → Int@ℓ+1` makes interpreter behavior observable at the meta‑level.

---

## Page 8 — Operational SOS with effect rows

Evaluation configurations: `⟨Σ, e, H⟩` with state `Σ`, expression `e`, and active handler stack `H`.

Small‑step rules (selected):

```
[E-App]  ⟨Σ, (e1 e2), H⟩ → ⟨Σ, e1, H⟩ → … → apply
[Op]     ⟨Σ, op(k), H⟩ → handle(op, k, H)
[Anti]   ⟨Σ, anti⟨e⟩, H⟩ → run e with H′=H∘no‑commit; return value; Σ unchanged
[Meta]   ⟨Σ, meta‑of(e), H⟩ → run e with inspector ops enabled
```

Determinism holds modulo handler nondeterminism; confluence is shown for a core where handlers are **commuting**.

---

## Page 9 — Denotational model (Eilenberg–Moore)

Let `Eff` be a monad on `Set` (or `CPO`) constructed from `State × Log × Tension`. Interpreters are **algebras** for syntax functor `S` in the Kleisli category `Kl(Eff)`:

```
α : S(Eff Val) → Eff Val
```

Handlers are **monad morphisms** `h : Eff⇒Eff′`.

**Theorem (Soundness).** If `h` is a monad morphism and `α` commutes with `h`, then transforming an interpreter by `h` preserves program meanings up to the image of `h` and preserves aboutness equivalence.

---

## Page 10 — Grounded dynamic frames

Bind §13 grounding to interpreters by adding **measurement handlers**:

```
measure : Spec → Eff Evidence
compare : Pred(SIT)×Evidence → Eff Err
```

A **grounded interpreter** `𝕀_g` is `𝕀` with measurement ops handled to enforce ε‑commuting grounding diagrams. Policies gate when to trust evidence and when to mark `⋈`.

---

## Page 11 — Fixed points of interpretation (guarded Y)

Interpreters can **interpret definitions of themselves** (macro systems, learned updates). We define a *guarded* fixed‑point operator over `Int`:

```
Y▸_Int(F) : Int    where  F : ▷Int → Int
Y▸_Int(F)  ≅  F (next Y▸_Int(F))
```

Contractivity via a step‑indexed metric (handlers must delay state‑modifying ops). Ensures productivity and avoids instantaneous self‑collapse.

---

## Page 12 — Confluence, stability, and safety

**Confluence (core).** For a commuting set of handlers `H` and terminating inner evaluation, the induced rewrite system for interpretation steps is confluent (Newman’s lemma).

**Stability.** Define spectral radius `ρ(DF|_*)` of the linearization of handler update near a fixed point; require `ρ<1` for stability. If violated, insert `anti` or increase delay depth.

**Safety.** Tower rule and explicit `↓` enforce non‑collapse; `anti` isolates speculative interpreters; `⋈` remains zone‑local.

---

## Page 13 — Interaction with regen `T = R∘U`

Interpreters call `regen` to canonicalize scenes before or after interpretation. We distinguish:

* **Pre‑regen:** `e ↦ T(e) ↦ 𝕀` reduces syntactic variability; helpful for robust parsing.
* **Post‑regen:** `𝕀[e]` produces scene `s`; apply `T(s)` to eliminate spurious differences while preserving aboutness.

**Coherence.** `𝕀∘T ≅ T∘𝕀` up to ANF when handlers are **structure‑respecting** and do not invent edges absent from input without budget.

---

## Page 14 — Paraconsistent zones and handler barriers

Introduce **zone‑typed handlers**:

```
handle_Z : Eff_ρ τ → Eff_ρ τ
```

that restrict updates to zone `Z`. If a contradiction arises, `mark⋈` annotates edges; selectors default to credal answers. Cross‑zone merges require explicit `fuse⟨Z_i,Z_j⟩` ops handled by a policy layer.

**Guarantee.** No handler may perform cross‑zone destructive updates without an `anti` preview and a recorded `collapse` decision.

---

## Page 15 — Algorithms and complexity

* **Handler normalization.** Compute a canonical order of commuting handlers (e.g., `prov ≺ state ≺ policy ≺ regen`). Complexity linear in number of ops.
* **Effect inference.** Infer minimal effect row `ρ_min(e)` for expression `e` by abstract interpretation; used to pick a lightweight interpreter.
* **Meta‑transform synthesis.** Given desired `ρ′`, synthesize transformer `τ : 𝕀⇒𝕀′` via monad morphism search; NP‑hard in general, tractable for fixed handler libraries.

---

## Page 16 — Worked examples I (language)

**Example A — Interrogative‑first interpreter.** A transformer `τ_Q` prepends a `selector` handler so that questions are answered **without** building full truth conditions; then a lazy truth handler backfills if needed.

**Example B — Meta‑of for contrastive parsing.** `meta‑of(𝕀)` exposes relators as objects to ask *why in vs on*. Handler logs alternative relators; `anti` prevents state commits during exploration; final choice applied through `collapse`.

---

## Page 17 — Worked examples II (self‑modifying agents)

**Policy‑learning interpreter.** `𝕀_θ` interprets scenes while updating a policy `π_θ`. Meta‑relator `trans` flips agent vs external perspective; difference drives a gradient step. `Y▸_Int` yields a steady policy interpreter under delay.

**Reflective debugger.** `anti⟨meta‑of(𝕀)⟩` allows an agent to inspect how an utterance would be interpreted, with provenance and tension surfaced, before committing the update.

---

## Page 18 — Diagnostics and metrics

* **Effect audit**: counts of ops per handler; distribution over zones.
* **Stability index**: change in state across re‑runs; should decay under fixed input.
* **Aboutness fidelity**: `≈̇` between pre/post regen outputs.
* **Grounding error** under protocols (§13).
* **Paraconsistent isolation**: leak rate of `⋈` across zones.
* **Transformer quality**: preservation of test suite answers after `τ`.

---

## Page 19 — JSON exports and APIs

**Interpreter capsule.**

```json
{
  "name": "I_core",
  "effects": ["state","prov","policy","regen"],
  "handlers": ["H_state","H_prov","H_policy","H_regen"],
  "zones": ["Z_core","Z_src:A"],
  "grounding_protocol": "pr#13",
  "version": "v0.1"
}
```

**Meta‑transform.**

```json
{
  "transform": "meta-of",
  "input": "I_core",
  "output": "I_meta",
  "laws": ["strong-monoidal","aboutness-preserving"]
}
```

**Run log.**

```json
{
  "expr": "where(on(cat,mat))",
  "interpreter": "I_meta",
  "ops": [
    {"op":"ask","args":{"wh":"where","phi":"on(cat,mat)"}},
    {"op":"prov","capsule":{"sensor":"vision#A"}}
  ],
  "zone":"Z_src:A",
  "result": ["mat#1"],
  "tension": false
}
```

---

## Page 20 — Next steps

1. Implement a reference `Eff` with state/prov/⋈/policy rows and composable handlers.
2. Provide `meta‑of`, `anti`, `trans`, `para‑through` as functors on `Int`, with proofs of coherence on a core.
3. Deliver a guarded fixed‑point engine `Y▸_Int` for self‑modifying interpreters.
4. Integrate grounding protocols (§13) and regen passes (§8); release audits, tests, and examples.

---

*End of Part IV §14: Meta‑Interpretation as Dynamical Frame (20pp v0.1).*


---


# MetaPrincipia Autopoietica — Part IV: Metasemantic Foundations

## §15. Minimal Conditions for Meaning to Emerge — Anchoring • Recursion • Coherence (Twenty‑Page Slab, v0.1)

> **Thesis.** Meaning emerges when a symbol system crosses a tri‑threshold of **Anchoring**, **Recursion**, and **Coherence** (ARC). Below ARC, symbols are noise or mere labels; at ARC, they become **about** structured situations and support learning, question‑answering, and control. We formalize ARC as necessary‑and‑almost‑sufficient conditions in the 𝒞\_A framework, give constructive procedures, and state falsifiable tests.

**Dependencies.** Part I (symbols, kinds), Part II §5–§8 (aboutness, axioms, barriers, regen), Part IV §13–§14 (grounding, interpreters as effects).

**Page map (20):**

1. Problem statement and design criteria
2. ARC triad: overview and intuition
3. Minimal symbol substrate
4. Axiom A — Anchoring
5. Axiom R — Recursion
6. Axiom C — Coherence
7. ARC ⇒ aboutness non‑degeneracy
8. ARC ⇒ compositionality at the margin
9. ARC ⇐ learning sufficiency (PAC‑style)
10. Emergence from untyped strings
11. Category‑theoretic core (limits/colimits)
12. Operational core (call‑by‑meaning)
13. Paraconsistent minimality (⋈‑safe)
14. Grounding protocols at low resource
15. Metrics for emergence
16. Reference experiments (toy → real)
17. Minimal engines and ablations
18. Failure modes and guards
19. JSON exports (ARC report)
20. Next steps

---

## Page 1 — Problem statement and design criteria

We seek **minimal** structural and algorithmic conditions under which a symbol system supports **meaningful** use: stable reference, composition, question answering, and update under evidence. Criteria:

* **Constructive** (buildable in finite resources).
* **Auditable** (capsules/logs at interfaces).
* **Paraconsistent** (no explosion under contradictions).
* **Groundable** (attaches to measurements per §13).

---

## Page 2 — ARC triad: overview and intuition

* **Anchoring (A).** There exist typed **anchors** that symbols can designate, with a non‑degenerate interface to observations and actions.
* **Recursion (R).** There is a guarded mechanism to build unbounded structures from bounded parts (lists/trees/paths; Y▸ or μ/ν).
* **Coherence (C).** There are constraints and normalization that align distinct constructions to a **canonical** aboutness up to torsion.

ARC delivers: *reference* (A), *productivity* (R), and *stability* (C).

---

## Page 3 — Minimal symbol substrate

Let `Σ_tok` be a finite token set. Minimal syntax:

```
Expr ::= a | (Expr Expr) | P[Expr] | Q(Expr)
```

where `a∈Atoms`, `P∈Relators`, `Q∈Selectors`. Types are the Part‑I core: `Thing, Prop, Rel, Question`.

**No assumptions** on grammar beyond application and parentheses. All structure arises from relator signatures and ARC axioms.

---

## Page 4 — Axiom A: Anchoring

**A1 (Anchor availability).** There exists a nonempty set `Anch ⊆ Thing` and a partial map `den : Strings → Anch` with observable support: for some sensor family `S`, `obs_S` can distinguish denotations with error ≤ ε.

**A2 (Role discriminability).** There exist at least two distinct roles `ρ1≠ρ2` such that incidents at `ρ1` are distinguishable from `ρ2` in observations. Formally, the confusion matrix between `ρ1,ρ2` under `obs_S` has off‑diagonal mass ≤ δ < 1/2.

**A3 (Measurement link).** For a nonempty relator set `Σ_R`, each `R∈Σ_R` has a measurement spec `μ_R` (§13) defining how `R(x,y)` can be tested/intervened.

**Minimal A.** A holds if (A1–A3) with ε,δ below policy thresholds; anchors may be latent but must be **distinguishable**.

---

## Page 5 — Axiom R: Recursion

**R1 (Guarded constructor).** There exists a contractive builder for scenes:

```
cons : Thing × ▷Scene → Scene
```

with `next:Scene→▷Scene` the delay; dually, a fold (catamorphism) exists for finite scenes.

**R2 (Fixed‑point facility).** A guarded Y‑operator is available (§11):

```
Y▸ : (▷X→X)→X
```

which ensures productivity and permits definitions of paths, lists, and recursive queries.

**R3 (Counter support).** A Peano object `N` exists (§10), enabling counting and iteration.

**Minimal R.** R holds if at least one guarded constructor with fold and an NNO is present.

---

## Page 6 — Axiom C: Coherence

**C1 (Normalization).** There exists an ANF canonicalizer `R∘U` (§8) such that for all expressions `e`, `|T(e)| = |e|` up to torsion `D*`, and `T` terminates.

**C2 (Constraint set).** A nonempty set of coherence constraints holds for basic relators (e.g., contact requires `Surface(y)` for `on(x,y)`; `in` nests). These are checkable or learnable; violations are marked `⋈` not global failure.

**C3 (Equivalence).** There exists an aboutness equivalence `≈̇` (role‑preserving hypergraph isomorphism) with a **precise role map**: a bijection on incident role labels for each hyperedge.

**Minimal C.** C holds if ANF exists and at least one nontrivial constraint is enforced; `≈̇` is total on well‑typed scenes.

---

## Page 7 — ARC ⇒ aboutness non‑degeneracy

**Theorem 15.1 (Non‑degeneracy).** If A,R,C hold, then there exists a nonconstant aboutness map `|·| : Expr→Hyp` such that two distinct expressions can yield distinct aboutness under some context, and `|·|` is stable under `T`.

*Sketch.* A ensures anchors and measurable relators; R ensures unbounded structure; C ensures canonicalization, preventing collapse of all expressions to a single hypergraph.

---

## Page 8 — ARC ⇒ compositionality at the margin

**Theorem 15.2 (Compositional margin).** Under ARC, there exists a fragment `𝔽⊆Expr` closed under application where `|e₁·e₂|` is determined by `|e₁|,|e₂|` and the relator signature, up to torsion. Moreover, selectors compute answers by role‑filtered queries on `|·|` (Part III §9).

*Sketch.* C1 gives ANF; R1 binds structure; A2 distinguishes roles so composition is not degenerate.

---

## Page 9 — ARC ⇐ learning sufficiency (PAC‑style)

**Theorem 15.3 (Learnability).** Suppose there is a distribution `𝒟` over situations and observation protocol `Pr`. If A holds with ε,δ < 1/4, R holds with bounded description length, and C holds with finite constraint set, then there exists a learner that with `m = Õ((d+log(1/δ′))/ε′²)` samples recovers an interpreter whose error on `𝒟` is ≤ ε′ with probability ≥ 1−δ′.

*Sketch.* Reduce to PAC learning of structured predicates with finite VC dimension determined by anchor classes and relator arities; C bounds hypothesis space via ANF; R supplies constructive bias via folds.

---

## Page 10 — Emergence from untyped strings

Start with strings and a partition of tokens into `{Relators, Selectors, Atoms}` by unsupervised criteria (mutual information with observation events). Then:

1. Propose anchors by clustering observations.
2. Propose relator signatures by testing intervention co‑variance.
3. Instantiate `T=R∘U`; iterate until ANF stabilizes.
4. Teach selectors by supervision from QA pairs.
5. Verify ARC: compute ε,δ; check guarded constructors and ANF termination.

**Guarantee.** If ARC is satisfied at thresholds, compositional QA accuracy rises above chance and stabilizes under re‑paraphrase.

---

## Page 11 — Category‑theoretic core (limits/colimits)

Minimal categorical requirements:

* **Finite products** in `Scene` for conjunction/substitution.
* **Coproducts** for alternative scenes.
* **Pullbacks** to instantiate role filling.
* **Pushouts** to glue under DPO (§12–§14).
  These suffice to realize ANF and basic QA; exponentials are optional.

**Proposition 15.A.** If `Scene` has pushouts along monos and finite limits, DPO rewriting terminates on finite graphs with a well‑founded measure and admits local confluence for a finite critical set.

---

## Page 12 — Operational core (call‑by‑meaning)

Use evaluation contexts of Part I with **call‑by‑meaning**: reduce relator arguments to anchors; build edges; apply `T`. Minimal rules:

```
E ::= [·] | R(E,t) | R(t,E) | Q(E)
Value ::= anchors, closed relator apps
Step: R(a,b) ↦ edge_R(a,b);   Q(φ) ↦ query(|φ|)
```

Barriers block non‑guarded meta‑ops.

---

## Page 13 — Paraconsistent minimality (⋈‑safe)

Even minimally, contradictions arise. Keep a **local logic** `Prop_⋈` with no explosion. Queries default to **credal** answers (intervals/sets) unless a collapse policy is invoked (§7). This is sufficient for stable progress of learning and QA without global consistency.

---

## Page 14 — Grounding protocols at low resource

Provide micro‑protocols (`≤ 10` steps) per relator: e.g., for `on(x,y)`, detect contact and support with simple sensors. Calibration with tiny ECE targets (≤0.05). Grounding success at ε assures A3.

**Bootstrap.** If no sensors, use *proxy* interventions (simulated environments) to prime signatures before transfer.

---

## Page 15 — Metrics for emergence

* **A‑score (Anchoring).** Mutual information `I(symbol; anchor)`; role confusion rate.
* **R‑score (Recursion).** Compression gain from recursive codes; success of length generalization.
* **C‑score (Coherence).** ANF stabilization steps; WL‑kernel distance variance under paraphrase.
* **QA fidelity.** Accuracy on who/where/what; invariance under negation/modality.
* **Grounding.** ε‑commutation rate (§13).
* **Paraconsistent isolation.** Leak rate from `⋈` zones.

---

## Page 16 — Reference experiments (toy → real)

**Toy 1 — Blocks world.** Train from demonstrations. Measure ARC: anchors=blocks, relators=`on/in/left_of`, recursion via stack depth; coherence via contact constraint.

**Toy 2 — Grid agents.** Commands composed recursively; measure generalization to longer paths.

**Real 1 — Caption QA.** Map captions to scenes; evaluate selectors; verify aboutness invariance across paraphrase.

**Real 2 — KB alignment.** Align text scenes to KG; measure coherence via DPO schema rules.

---

## Page 17 — Minimal engines and ablations

* **Engine‑M0 (baseline).** Bag‑of‑words anchors; no R; no C → fails QA beyond labels.
* **Engine‑M1 (A only).** Anchors + single relator; no recursion → limited, no compositional growth.
* **Engine‑M2 (A+R).** Can build lists/paths but drifts without C; QA unstable.
* **Engine‑M3 (A+C).** Stable but finite; lacks productivity.
* **Engine‑ARC (A+R+C).** Passes compositional QA, stable under paraphrase, supports learning.

Ablate each axis; report metric drops.

---

## Page 18 — Failure modes and guards

* **Anchor over‑merging.** Coref errors collapse distinct anchors. Guard with provenance and thresholds.
* **Spurious recursion.** Unguarded self‑application oscillates; enforce `next` and step indices.
* **Over‑normalization.** Coherence deletes valid diversity; keep alternative zones and counterfactual store.
* **Underspecified measurement.** No causal tests; flag non‑identifiability (§13).
* **Torsion misuse.** Synonymy rules leak across roles; segregate torsion dictionaries by context.

---

## Page 19 — JSON exports (ARC report)

```json
{
  "arc_report": {
    "system": "demo#ARC",
    "A": {"I_symbol_anchor": 0.42, "role_confusion": 0.08, "grounding_eps": 0.04},
    "R": {"compression_gain": 0.27, "length_gen_acc": 0.81},
    "C": {"anf_steps": 3, "paraphrase_var": 0.06},
    "QA": {"who": 0.89, "where": 0.93, "what": 0.86},
    "paraconsistency": {"leak_rate": 0.01},
    "notes": "blocks+caption mixed; torsion v1.2"
  },
  "grounding_capsules": [ {"relator":"on","protocol":"pr#7","ece":0.03} ],
  "ablations": ["M1","M2","M3"]
}
```

---

## Page 20 — Next steps

1. Release minimal 𝒞\_A runtime with anchors, one guarded constructor, and ANF.
2. Provide micro‑protocols for two relators and selector QA.
3. Publish ARC benchmark tasks and scorer.
4. Extend to continuous domains (vision/audio) with proxy grounding.
5. Formalize tight lower bounds for A,R,C thresholds under realistic noise.

---

*End of Part IV §15: Minimal Conditions for Meaning to Emerge (20pp v0.1).*


---

# MetaPrincipia Autopoiētica — Part IV: Metasemantic Foundations

## §16. Toward a General Theory of Autopoiēsis in Cognition — Fractal Semantics; Semiotic Recursion as a Living Structure (Twenty‑Page Slab, v0.1)

> **Thesis.** Autopoiēsis in cognition is a **multiscale regeneration process** that maintains an identity of meaning across transformations. The semantic substrate is **fractal**: self‑similar patterns of aboutness repeat over scales; production and interpretation form a **semiotic recursion** that preserves invariants under regen `T = R∘U`, barriers, and grounding protocols. We give state equations, categorical structure, metrics, algorithms, and tests.

**Prereqs.** Part I (symbol system), Part II §5–§8 (aboutness, axioms, barriers, regen), Part III §9–§12 (language, agents, KGs), Part IV §13–§15 (grounding, meta‑interpretation, minimal emergence).

**Page plan (20).**

1. Problem and scope
2. Cognitive autopoiēsis: formal definition
3. Fractal semantics: scale operators
4. Semiotic recursion: production/interpretation cycle
5. Dynamical core: state equations and attractors
6. Multiscale operators: coarse‑grain, refine, renormalize
7. Fractal metrics: dimension and entropy of aboutness
8. Growth and viability laws
9. Homeostasis and control
10. Structural coupling with environment
11. Multi‑agent autopoiesis
12. Category‑theoretic formulation
13. Fixed points and morphogenesis
14. Stability, tension, and collapse control
15. Algorithms for multiscale maintenance
16. Benchmarks and evaluation
17. Worked examples
18. Implementation sketch
19. JSON schemas
20. Next steps

---

## Page 1 — Problem and scope

Goal: specify necessary and near‑sufficient structure for **self‑maintaining cognition** where meaning persists under ongoing transformation. Deliverables:

* State‑space and operators for autopoietic maintenance.
* Multiscale semantics with explicit scale maps.
* Proof obligations for invariants and safety.
* Algorithms and benchmarks.

Constraints: paraconsistency (`⋈` local), tower rule (no meta‑collapse), grounding protocols (§13), interpreter effects (§14), minimal ARC conditions (§15).

---

## Page 2 — Cognitive autopoiēsis: formal definition

Let `Σ = ⟨KG, Pol, Int, Env⟩` where `KG` is an aboutness hypergraph with zones, `Pol` policies, `Int` interpreter stack, `Env` external channels. Define **autopoietic update** over discrete time `t`:

```
KG_{t+1} = T ∘ A_{Pol_t,Int_t}( KG_t, Obs_t, Cmd_t )
Pol_{t+1} = U_Pol( Pol_t, Logs_t )
Int_{t+1} = U_Int( Int_t, Data_t )
```

The system is **autopoietic** on horizon `H` if there exists a nonempty set of invariants `Inv` such that for all `τ≤H`:

```
Inv(KG_{t+τ}) holds and |KG_{t+τ}| ≈̇ |KG_t| on protected cores
```

with deviations bounded by budgets.

**Core invariants.** Identity anchors, role dictionaries, schema constraints, grounding error ≤ ε, tension leak ≤ λ.

---

## Page 3 — Fractal semantics: scale operators

Define **scale maps** on hypergraphs:

* **Coarsen** `S_↓^k : Hyp → Hyp` merges anchors/edges within radius `k` under torsion dictionary `D*` and attribute thresholds.
* **Refine** `S_↑^k : Hyp → Hyp` splits anchors via latent variables or sensor resolution.

**Fractal self‑similarity.** A region `Z` is **self‑similar** if there exists `k>0` and an isomorphism `ϕ` with

```
S_↓^k( Z ) ≅ ϕ(Z)
```

Define a **fractal semantics** when the distribution of motif subgraphs `Motif_m` is approximately scale‑invariant (power‑law tails) and semantic answers (selectors) are invariant up to ε under `S_↓^k`.

---

## Page 4 — Semiotic recursion: production/interpretation cycle

Two maps:

```
Produce : KG × Goals → Expr
Interpret: Expr × KG → KG × Answers × Logs
```

Cycle:

```
KG_t ─Produce→ e_t ─Interpret→ KG_t′ ─T→ KG_{t+1}
```

**Semiotic recursion** holds if the composition preserves `Inv` and improves task utility or calibration. The interpreter is an effect (§14); `T` canonicalizes outputs (§8).

---

## Page 5 — Dynamical core: state equations and attractors

Let `x_t` encode summaries: `(|KG_t|, Err_t, Tension_t, Capacity_t, Utility_t)`.
Dynamics:

```
x_{t+1} = F(x_t, u_t, w_t)
```

where `u_t` are actions/policies and `w_t` environment noise.

**Attractor semantics.** An **autopoietic attractor** is a compact set `A` with:

* forward invariance under `F`,
* bounded error `Err≤ε`,
* bounded tension growth and non‑explosion,
* positive utility or competence gain.

---

## Page 6 — Multiscale operators: coarse‑grain, refine, renormalize

Define an **RG‑like** operator on interpreters and KGs:

```
ℛG_k(KG,Int) = ( S_↓^k ∘ KG ,  Renorm_k(Int) )
```

`Renorm_k` rescales thresholds, handler orders, and budgets. **Fixed point:** `(KG*,Int*)` such that `ℛG_k(KG*,Int*) ≈ (KG*,Int*)` up to isomorphism and parameter rescaling.

**Law (coherence).** Answers to coarse queries commute with `ℛG_k` to within ε on protected roles.

---

## Page 7 — Fractal metrics: dimension and entropy of aboutness

Define **box‑counting dimension** on `|KG|`:

```
N(r) = minimal # of balls of radius r (in role‑aware graph metric) to cover anchors
D_B = lim_{r→0}  log N(r) / log(1/r)
```

Define **topological semantic entropy**:

```
h_top = lim_{n→∞} (1/n) log #distinct aboutness motifs of size ≤ n
```

Also define **answer entropy** for selectors under distribution of queries. These quantify richness and compressibility.

---

## Page 8 — Growth and viability laws

Empirical laws expected in living semantics:

* **Zipf–Heaps behavior** for anchor/edge types.
* **Power‑law** in motif counts.
* **Logistic or Gompertz** growth of capacity with saturation.

Define **viability kernel** `V` in state space where constraints hold. **Viability law:** policies must keep `x_t ∈ V`; regen and handler schedules act as controls.

---

## Page 9 — Homeostasis and control

Control objective:

```
min_π  E[ Σ_t L(x_t, u_t) ]
```

with losses combining error, tension, compute cost, and missed utility.

**Controllers.**

* Proportional on `Err` with barrier gating.
* Integral on calibration gaps.
* Model‑predictive using simplified `F`.

**Lyapunov candidate** `V(x)=α Err + β Tension + γ Drift`; show decrease under policy in normal regimes.

---

## Page 10 — Structural coupling with environment

Define **coupling map** `C : Env × KG → Env × KG`. Structural coupling holds when joint dynamics has a **product‑like attractor** where regularities in Env align with motifs in KG via `J` (§13). `C` preserves grounding errors within bands.

Perturbation tests: scrambling `Env` or handler order should degrade but not destroy core invariants.

---

## Page 11 — Multi‑agent autopoiesis

Agents `A_i` exchange scenes over protocols (§12). Define **ecosystem operator**:

```
Ecos( {KG_i,Int_i} ) = CRDT_merge + Policy_align + DPO_maint
```

A system is **autopoietic plural** if each agent maintains its invariants and the consortium maintains shared motifs with bounded divergence. Use CRDT for adds; serialize collapses via logs.

---

## Page 12 — Category‑theoretic formulation

Scales form an **indexed category** `Scene_{λ}` with reindexing functors `S_↓, S_↑`. Regen is a monad `T` on each fiber; context is a comonad `▢` (environmental view). Autopoiēsis is a **bialgebra** structure:

```
α: S( Eff Val ) → Eff Val      // interpreter algebra in Kl(Eff)
δ: Val → ▢ Val                  // contextual co‑algebra
```

Compatibility laws enforce coherence under scale change and regen.

---

## Page 13 — Fixed points and morphogenesis

Define **shape equations** for motifs `M`:

```
M ≅ F( S_↓^k(M), Params )
```

with guarded Y to solve. Morphogenesis is the emergence of stable motifs as fixed points of structure maps. Selectors act as **probes** to verify shapes.

---

## Page 14 — Stability, tension, and collapse control

Use **tension volume** `|C_Z|` per zone and **flux** between zones. Define **meltdown indicator**

```
Λ = ρ(DF|_*) ∨ (Δ|C|/Δt > θ) ∨ (flux > φ)
```

If `Λ` true, insert `anti`, increase delay, reduce regen budget, or quarantine zones. Guarantee: non‑explosion and tower safety.

---

## Page 15 — Algorithms for multiscale maintenance

1. **Scale schedule.** Periodically apply `S_↓^k` to form summaries.
2. **Two‑pass QA.** Answer at coarse scale; refine if confidence low.
3. **RG fine‑tuning.** Update handler thresholds via `Renorm_k`.
4. **Motif cache.** Maintain frequent subgraphs with WL hashing.
5. **Counterfactual store.** Keep losing collapses in `Z_alt` for rollback.
6. **Paraconsistent query processing.** Return intervals unless strict.

Complexity mostly linear in edges per scale; caches amortize matching.

---

## Page 16 — Benchmarks and evaluation

Metrics:

* **Fractal metrics** `D_B, h_top` stability.
* **Grounding** ε under interventions.
* **QA throughput/latency** with two‑pass.
* **Autopoietic resilience** under perturbations (sensor dropout, policy noise).
* **Ecosystem divergence** across agents.
* **Safety**: leak rate of `⋈`, down‑lift audit counts.

Benchmarks: blocks‑world, caption‑QA, multi‑agent knowledge fusion, long‑horizon task loops.

---

## Page 17 — Worked examples

**Example 1 — Fractal stories.** Scenes for narratives show motif self‑similarity (goal, obstacle, resolution) across chapters and sentences. `S_↓` compresses to plot graph; QA preserved.

**Example 2 — Visual scenes.** Repetitive textures and object arrays; motifs repeat across scales; selectors answer counts first at coarse scale.

**Example 3 — Multi‑agent science team.** Agents propose hypotheses; motifs are experimental cycles; CRDT merge maintains protocol motifs; collapses logged.

---

## Page 18 — Implementation sketch

Data:

* Zone‑typed hypergraph with role labels and capsules.
* Scale layers with pointers `parent/children`.
* Motif cache with WL fingerprints.
* Handler stack with effect rows.

Pseudocode (high‑level):

```
loop t:
  Hc = S_↓^k(KG)
  ans, conf = QA(Hc, q)
  if conf < τ: ans = QA_refine(KG, q)
  KG = T( Interpret( Produce(KG, goals), KG ) )
  if meltdown(Λ): apply_guards()
  update_handlers_via_Renorm()
```

---

## Page 19 — JSON schemas

**Scale layer.**

```json
{
  "layer": k,
  "nodes": ["n#…"],
  "edges": ["e#…"],
  "parent": "layer#k+1",
  "children": ["layer#k-1"],
  "torsion": "D*#v1",
  "metrics": {"db": 1.72, "htop": 3.1}
}
```

**Motif capsule.**

```json
{
  "motif_id": "m#…",
  "fingerprint": "wl:…",
  "roles": ["Theme","Location"],
  "scale_invariant": true,
  "support": 124
}
```

**Autopoiesis report.**

```json
{
  "identity_core": ["anchor#…"],
  "invariants": ["grounding<=0.05","leak<=0.01"],
  "fractal": {"db": 1.68, "htop": 2.7},
  "safety": {"downlifts": 2, "leak": 0.004}
}
```

---

## Page 20 — Next steps

1. Implement `S_↓, S_↑`, RG loop, and motif caches in the reference runtime.
2. Add two‑pass QA and scale‑aware selectors.
3. Release resilience benchmarks and autopoiesis reports.
4. Prove compositional preservation theorems for selectors under `S_↓`.
5. Extend to continuous time and stochastic differential forms.

---

*End of Part IV §16: Toward a General Theory of Autopoiēsis in Cognition (20pp v0.1).*
