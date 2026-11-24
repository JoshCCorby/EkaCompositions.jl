# Evaluation roadmap: rigorous recovery, controls and scaling

Prepared 14 September 2026 from repository state
`0629ba9d600afcd0cdbf1ddfc30ef83dbe6088c4`. The working tree contained the
untracked owner file `PROJECT_BRIEF.md`; it was read for context and not changed.
This document proposes the next stage. It does not amend the four frozen
protocols, reinterpret their results, or authorize a new real-data run.

## Executive recommendation

Do not add PyTorch now. Eka already has the important scientific foundation:
composition-safe positive–unlabelled (PU) recovery, a whole-chemical-system
holdout, three defensible references, a fixed element-pair factor comparator,
label-sensitivity analysis, independent Python checks and exact local reruns.
The highest-value next step is to make the evaluation layer reusable and
system-aware, then add one direct observed-pair control and one prospectively
specified missing-pair ablation.

Use chemical-system holdout as the primary generalisation protocol. Retain
composition holdout as an interpolation control, not as the headline discovery
test. Keep composition Hits@100 as the primary operational outcome because it
answers “how many known positive-provenance formulas are recovered in a fixed
screening budget?” Add macro Recall@100 to expose changing holdout sizes and a
system-level recovery diagnostic so that many stoichiometries from one element
system cannot masquerade as many independent discoveries.

The most important limitation is upstream of modelling: this is retrospective
recovery inside a fixed Materials Project (MP) catalogue. The positive label is
an experimental-provenance proxy, the unlabelled class is not a negative class,
and the candidate universe consists of already catalogued formulas. No model or
metric extension can turn this dataset into evidence of synthesizability or
prospective discovery.

## A. Current state

### A.1 Two ranking products that must remain distinct

The repository has two separate tasks.

1. The SQLite query path in `src/database.jl` retrieves stored composition/score
   rows subject to element, arity and score-threshold filters. `rank!` in
   `src/ranking.jl` orders those rows by either stored score or cosine similarity
   to one supplied reference. It does not fit a model or evaluate held-out
   recovery. Its generic tie rule is descending ranking value, descending stored
   score, then canonical formula.
2. The MP research path audits and groups a fixed MP snapshot, creates PU
   holdouts, fits or constructs training-only scorers, ranks a complete candidate
   pool and evaluates deliberately hidden positive-provenance compositions.
   This path has its own score-independent tie hash and does not inherit the
   SQLite stored-score tie breaker.

The public `benchmark_rankings` path in `src/benchmark.jl` is a third, narrower
interface for an explicitly binary-labelled pool. It already reports fixed-budget
hits, precision, recall, enrichment and simple coverage proxies. Its contract
correctly warns that it is inappropriate when “0” merely means unobserved.

### A.2 Composition, candidate and positive definitions

`Composition` in `src/compositions.jl` accepts simple formulas with valid element
symbols and positive integer amounts. It combines repeated symbols, reduces the
amounts by their greatest common divisor and alphabetically orders the symbols.
Equality and hashing therefore collapse element permutations and proportional
spellings such as `MgZn`, `Zn2Mg2` and `Mg2Zn2`.

For the MP workflow, `audit_mp_snapshot` in `src/mp_audit.jl` first verifies the
snapshot metadata and checks that `records.jsonl` normalises to `records.tsv`.
It then groups every polymorph/record by canonical reduced composition. Within a
group:

- **positive** means at least one record has `theoretical=false`;
- **unlabelled** means every record has `theoretical=true`;
- **unresolved** means no positive record exists and at least one flag is
  missing.

The fixed real snapshot records 24,020 MP records, 12,506 canonical compositions,
5,359 positives, 7,147 unlabelled compositions, no unresolved compositions and
1,343 mixed true/false groups. The scope is oxygen plus exactly two other
elements; it is not an oxidation-state-validated oxide set. These counts are in
`reports/local/mp-ternary-audit/audit.toml` and summarised in
`docs/recovery-findings.md`.

In `mp_recovery_splits` (`src/mp_recovery.jl`), a composition-holdout candidate
pool is the union of a hash-selected fifth of positive compositions and every
eligible unlabelled composition. Training contains the remaining positives.
For the original policy, each of the 20 real splits has 4,288 training positives,
1,071 held-out positives and 8,218 candidates.

In `system_splits` (`src/mp_system_holdout.jl`), a chemical system is the sorted
set of element symbols, ignoring stoichiometry. A hash-selected fifth of the
eligible system universe supplies candidates: all held-out positives and
unlabelled formulas in those systems. Training positives come only from other
systems. Depending on label policy and seed, the real system-holdout pools have
2,096–2,710 candidates and 740–1,171 held-out positives.

Thus a **candidate** is an eligible, already catalogued canonical composition in
the evaluator-owned pool. It is not a formula newly generated by Eka. A
**recommendation** is a candidate selected from the top of a complete deterministic
ranking. A **relevant item** is a deliberately held-out positive-provenance
composition under the active label policy. There are hundreds or thousands of
relevant items per split, not one relevant item per query.

### A.3 Filtering and label isolation

Filtering occurs before ranking and is explicit:

- the API snapshot query requires oxygen, exactly three elements, non-deprecated
  records and `include_gnome=false`;
- the audit excludes invalid/nonintegral formulas and anything outside scope;
- unresolved groups are outside training and evaluation;
- the selected label policy either retains, excludes or unlabels mixed groups;
- system holdout keeps candidate formulas only in selected systems, so eligible
  unlabelled formulas in other systems are deliberately unused;
- no post-score threshold removes candidates, and budgets are rejected rather
  than truncated when `K` exceeds the pool;
- the element-pair model retains cold candidates with score zero and an explicit
  coverage flag instead of dropping them.

`pu_rank` accepts training formulas, candidate formulas, method and seeds, but no
labels, IDs or stored scores. `pu_metrics` receives held-out labels only after the
ranking exists. Tests in `test/test_mp_pu.jl`, `test/test_mp_label_sensitivity.jl`
and `test/test_mp_system_holdout.jl` check label isolation, refitting, membership
disjointness, deterministic order and tamper rejection.

### A.4 Methods already implemented

The PU workflow already includes:

- a deterministic SHA-256 pseudorandom ranking plus an exact uniform-random
  expected hit count;
- training-element popularity, counting each element once per unique training
  composition;
- maximum cosine similarity between a candidate's reduced stoichiometric vector
  and any training composition;
- a rank-four symmetric nonnegative element-pair factor model in
  `src/element_pair_model.jl`.

The learned model constructs a 117×117 matrix over non-oxygen elements. Each
training composition increments its unordered non-O pair. It fits nonnegative
factors to log-scaled counts with weight 1 on observed pairs, weight 0.01 on
unobserved pairs, L2 regularisation 0.01 and deterministic projected-gradient
descent. Candidate score is the factor dot product for its non-O pair. All
stoichiometries in the same chemical system therefore receive the same model
score.

The model is not a Seko reproduction. Its missing-pair penalty is a disclosed
implicit-feedback assumption, not a claim that missing compounds are negative.
The primary 2,000-iteration study had 101 capped fits out of 120. A later
20,000-iteration stability run converged all fits; 55 formerly capped top-100
sets changed, with up to 48 replacements, although hit deltas averaged +0.16 and
ranged from -5 to +4. The frozen 2,000-iteration result remains primary.

### A.5 Results already established

The completed comparisons make several proposed “future” tasks unnecessary:

- Under original composition holdout at K=100, maximum similarity exceeded
  popularity by only 0.50 mean hits across 20 overlapping splits.
- Under original system holdout, similarity trailed popularity by 14.45 mean
  hits at K=100.
- The element-pair model was essentially tied with popularity under original
  composition holdout (-0.20 mean hits) and exceeded it under original system
  holdout (+7.95 mean hits).
- Label-policy branches, all four budgets and unfavorable outcomes are retained.
- Post-hoc diagnostics show that the original system-holdout model's top 100
  contained about 13.5 systems, about 9 positive-hit systems and only about 5.68
  effective hit systems on average. Composition-level Hits@100 therefore does
  not represent 100 independent chemical decisions.

These are descriptive results over overlapping repeated holdouts. The repository
correctly makes no confidence-interval, significance, synthesis-success or causal
claim from them.

### A.6 Validation and provenance already present

The project is unusually strong here. Frozen protocol documents are content-hash
pinned in `src/mp_recovery.jl`. Split and run bundles retain source/input hashes,
membership hashes, implementation hashes, configuration, seeds, Julia/package
versions, complete rankings and metric denominators. Python analyzers independently
reconstruct membership, baseline scores, ordering and metrics. Separate-checkout
reruns reproduced deterministic outputs; runtime files are explicitly excluded
from byte equality.

Real snapshots, record-level rankings, factors and complete environments remain
under ignored `data/local/` and `reports/local/` paths. This preserves source
release hygiene but means a public checkout cannot exactly reproduce the real
results without the separately retained inputs.

## B. Scientific task definition

### B.1 Prediction task

For each outer split `s`, let:

- `T_s` be the canonical positive-provenance training compositions;
- `C_s` be the complete eligible candidate pool;
- `R_s ⊂ C_s` be the deliberately hidden positive-provenance compositions;
- `f_m(c; T_s)` be method `m`'s score using only permitted training information;
- `π_ms` be the deterministic complete ordering of `C_s`.

The task is: **rank `C_s` so that members of `R_s` appear early**. This is
masked-entry recovery from a positive–unlabelled catalogue. It is not binary
classification, candidate generation, crystal-structure prediction, stability
prediction or prospective synthesis recommendation.

The relevant set is `R_s`. It is complete with respect to the positives deliberately
masked by the split, but it is not complete with respect to all scientifically
viable materials because the unlabelled pool can contain viable compounds.

### B.2 Natural evaluation unit

The natural statistical/reporting unit is an **outer split and its ranked
candidate pool**. The ranked item is a canonical composition. There is no natural
per-user or per-reference “query,” so query-averaged recommender metrics should
not be imported by analogy.

Chemical system is an important secondary unit because formulas within a system
are clustered and the element-pair model assigns them identical scores. Report
both composition recovery and system recovery; do not silently replace one with
the other because they answer different screening questions.

### B.3 Meaningful budgets

Retain K = 20, 50, 100 and 200 for continuity with every frozen study. K=100 is
the primary fixed screening budget. The smaller and larger budgets describe the
recovery curve and cutoff sensitivity. They are not percentiles: K=100 is about
1.2% of an original composition-holdout pool but roughly 3.7–4.8% of a system
holdout pool. Consequently, compare methods within the same split first; comparisons
between split designs must show pool size and prevalence.

If a system-ranked diagnostic is added, choose its system budgets from pre-score
population counts and a stated experimental decision capacity, then freeze them.
Do not choose them after viewing method performance.

## C. Gaps

1. **Metrics are embedded in workflow code.** `pu_metrics` returns only the
   existing composition-level fixed-budget fields. There is no reusable relevance
   metric type, system-level evaluator or single schema shared by the binary and
   PU paths.
2. **Clustered recovery is not a first-class metric.** Effective/unique hit-system
   summaries exist only in a post-hoc Python diagnostic. A method can receive many
   composition hits from a few systems, especially when its score is constant
   within system.
3. **The learned representation lacks its most direct control.** The factor model
   is compared with element popularity and composition similarity, but not with
   the raw training pair count that it factorises. That control is necessary to
   show whether low-rank completion adds value beyond memorising observed pairs.
4. **The missing-pair assumption is unablated.** Weight 0.01 is a major modelling
   choice. Current code rejects zero, so an observed-pairs-only ablation would be
   a new, prospectively frozen experiment.
5. **Optimisation status complicates the headline model result.** Most primary
   fits hit the 2,000-iteration cap, and many rankings changed at 20,000 iterations.
   The stability evidence is good, but any next model comparison should use a
   convergence rule or fixed-compute claim defined before scoring.
6. **The primary split should be stated more strongly.** Composition grouping
   blocks exact duplicates and polymorph leakage, but composition holdout permits
   same-system stoichiometries and close analogues in training. System holdout is
   the more defensible headline for transfer to unseen element combinations.
7. **No protocol tests a genuinely new material or time period.** The snapshot
   lacks defensible first-discovery timestamps, and all candidates already occur
   in MP. Chronological or prospective claims are unavailable.
8. **Provenance is comprehensive but not uniform.** Core result configs do not
   consistently store a Git commit plus dirty-tree digest, Python environment,
   OS/architecture/CPU, thread counts or one common result schema. Source hashes
   are stronger than a commit alone, but restoration currently depends on
   experiment-specific packaging.
9. **Performance evidence is split across scripts and reports.** There are useful
   measurements but no isolated benchmark environment, scaling grid or end-to-end
   phase timings. Cumulative allocations are sometimes available; peak resident
   memory is not.
10. **Public reproducibility is deliberately incomplete.** Real data and detailed
    outputs are local pending artifact review. Public claims must stay within the
    aggregate evidence that can be shared and attributed.

## D. Recommended evaluation design

### D.1 Primary protocol: repeated chemical-system holdout

Use the existing v2 definition as the foundation: hash-select whole canonical
element sets, fit on positive compositions outside those systems, and rank all
eligible held-out-positive plus unlabelled formulas inside the selected systems.
This supports the narrow claim:

> recovery of MP positive-provenance compositions when their exact element
> combination is absent from positive training data.

It prevents exact composition leakage, proportional/permuted formula leakage,
polymorph leakage and same-element-system stoichiometric leakage. It does not
prevent transfer through chemically analogous systems, periodic-family neighbours
or each element's occurrence with other partners. That remaining information is
intentional for the element-pair task and must be stated.

Retain the 20 deterministic split seeds for continuity, but treat them as
overlapping sensitivity analyses, not independent replicates. Report every split.
Use macro means/medians across splits as the main aggregate so each split receives
equal weight. A pooled micro recall can be supplied only as a labelled diagnostic;
it weights splits with more held-out compositions more heavily and should not
replace macro summaries.

### D.2 Interpolation control: repeated composition holdout

Retain the existing composition holdout as a secondary control. It simulates
recovering missing formulas when other stoichiometries or formulas in the same
element system may already be known. It is scientifically useful for database
completion and for quantifying how much a method depends on local analogues. It
does not support a claim of transfer to unseen chemistry.

### D.3 Optional later stress test: leave-one-element-out

If a cold-start question becomes important, prospectively define a
leave-one-nonoxygen-element-out protocol over elements with adequate positive and
unlabelled support. Training must exclude every formula containing the held-out
element; candidates contain that element. This tests transfer to an unseen element,
not merely an unseen pair. It is expected to expose the element-pair model's
documented zero-score fallback and is valuable as a limitation test, not as a
route to a favorable score.

Do not call this “leave-one-chemical-family-out.” The repository has no validated
chemical-family taxonomy. Do not add a chronological split until a source with
defensible observation/discovery dates is obtained; MP snapshot or creation
timestamps are not sufficient.

### D.4 Leakage map and split-local recomputation

| Leakage path | Current protection | Remaining risk / required rule |
| --- | --- | --- |
| Formula order and overall scale | `Composition` canonicalisation before grouping | Keep canonicalisation deterministic and versioned. |
| Multiple MP structures/polymorphs | Group all records by composition before splitting | Never sample records or weight by structure count. |
| Same-system stoichiometries | Prevented by primary system holdout | Allowed only in the interpolation control and labelled as such. |
| Related periodic/chemical families | Not prevented | Requires a separately defined taxonomy or leave-element-out test. |
| Mixed theoretical flags | Three existing label policies | Keep policy-specific membership, fitting and denominators separate. |
| Source-dataset duplicates | Formula grouping collapses same formula; source IDs are not features | Cross-source correlated families remain; a source holdout needs a defensible source definition. |
| Global fitted statistics | PU rankers and factor model refit per split | Every new normaliser, vocabulary learned from data, sampler and cache must be fit inside the outer training split. |
| Candidate/test labels in scoring | Ranker signatures exclude labels; tests enforce isolation | Candidate membership is evaluator constructed. Never expose held-out labels, provenance fields or full-data counts to fitting. |
| Candidate filtering after scores | No post-score filters now | Freeze eligibility before scoring; invalid/excluded items are not denominator members and must remain counted in audit summaries. |
| Hyperparameter selection | Current learned model was frozen without tuning | Any tuning needs an inner training-only split matching the outer grouping; refit on all outer training data after selection. |
| External stored scores | Excluded because training independence is unknown | Include only after score-training data and candidate coverage are proven independent. |

Audit-time syntax normalisation and global formula grouping may use the complete
snapshot because they define immutable item identity and prevent duplicate
leakage; they must not compute predictive statistics. Label-policy construction
may inspect provenance because it belongs to the evaluator, but model inputs may
contain only the resulting permitted training formulas.

### D.5 Primary metrics

Use the smallest set that answers the screening question and keeps changing
denominators visible.

1. **Composition Hits@100.** Number of held-out positive-provenance formulas in
   the first 100. This is the primary operational measure. At a fixed screening
   budget it has a direct meaning and preserves all existing comparisons.
2. **Composition Recall@100.** Hits@100 divided by the split's held-out positive
   count. This is necessary when system-holdout relevant-set sizes differ. Call it
   “held-out recovery recall,” not sensitivity to true viable materials.
3. **Paired ΔHits@100.** Within each identical split/candidate pool, report the
   method-minus-popularity difference and method-minus-raw-pair-frequency
   difference. This is the primary comparative statistic rather than a standalone
   retrieval metric. Retain every split, mean, median, range and sign counts.

Always show `N`, `|R|`, prevalence and the analytical uniform-random expected
hits beside these metrics. Precision@100 is algebraically Hits@100/100 and need
not be a separate headline number; the current name `observed_label_fraction`
is scientifically safer because unlabelled is not negative.

### D.6 Secondary diagnostic metrics

- Hits and recall at K = 20, 50 and 200 to show budget sensitivity.
- Observed-label enrichment over split prevalence. This helps compare pools with
  different prevalence but does not correct selection bias in the catalogue.
- **Distinct positive systems@K**, **system recall@K** (held-out systems with at
  least one recovered formula / held-out systems) and the already used effective
  hit-system count. These expose clustered hits without changing the composition
  screening budget.
- A separately ranked system diagnostic, using one prospectively defined aggregate
  score per system and deterministic system ties, only if the scientific decision
  is genuinely system-level.
- Binary NDCG@K as an optional position-sensitive diagnostic. With binary held-out
  relevance it asks whether recovered positives occur near the very top, and its
  ideal denominator is well defined per split. It should not replace Hits@K.
- Score coverage/cold-candidate count, distinct-score count, tie-block sizes and
  whether a tie crosses K.
- Candidate-to-training similarity distributions and the share of candidates
  sharing systems with training; these diagnose split difficulty rather than
  model quality.
- Unique selected systems, effective selected systems and element coverage for
  list-composition diagnostics. Call them diversity/coverage proxies, not chemical
  diversity or novelty.

Do not add MRR: the first recovered item discards almost all information when
hundreds of positives are relevant. Do not add hit rate: “at least one hit” will
usually saturate at these budgets. Do not make MAP primary: there is one global
ranking per split rather than many user/query rankings, and average precision
implicitly gives meaning to the complete rank tail. Do not report exact-formula
novelty because every held-out candidate is composition-disjoint by construction.
NDCG and MAP also inherit the incomplete-ground-truth limitation of every PU
metric; an unlabelled formula can be scientifically valuable while counted as
nonrelevant.

### D.7 Ties, duplicates and denominators

- Preserve exact score equality. Do not round or use tolerance bins before
  ordering.
- Use the existing score-independent SHA-256 tie key and canonical formula
  fallback for PU composition rankings. Record the tie seed and algorithm ID.
- If system rankings are added, derive a separate versioned system tie key from
  the canonical system string. Do not let the number of formulas in a system
  decide ties accidentally.
- Reject duplicate canonical candidates before scoring. Do not deduplicate a
  ranked output after the fact.
- Define `N` and `R` after all protocol eligibility rules but before scoring.
  Invalid, out-of-scope, unresolved and policy-excluded groups are audit counts,
  not metric denominators. Under system holdout, eligible formulas in unselected
  systems are also outside that split's denominator.
- Never drop an unscorable candidate. Use an explicit fallback/coverage state and
  keep it in `N`, as the element-pair implementation already does.
- When exclusion changes eligibility, compact ranks before applying K and record
  the original rank depth, following the existing label-sensitivity implementation.

### D.8 Baselines and ablations

Retain random only as calibration: one deterministic hash ranking per split plus
the analytical expectation. It is not evidence that a learned method is useful;
the serious comparisons are below.

| Comparator | Scientific question | Exact inputs and score | Fit? | Expected cost | Evidence the factor model adds value |
| --- | --- | --- | --- | --- | --- |
| Training-element popularity (existing) | Does the model beat historical marginal element frequency? | Training formulas only; mean occurrence fraction of each candidate's three distinct elements. | Count frequencies per split. | O(Ta + Na + N log N), with arity `a=3`. | Positive paired ΔHits@100 and system-recovery diagnostics across predeclared policies/splits, not just one favorable mean. |
| Maximum composition cosine (existing) | Is retrieval explained by proximity to one known stoichiometric analogue? | Training and candidate reduced count vectors; maximum cosine to any training formula. | Build training vectors per split; no learned parameters. | O(NTa² + N log N), streamed. | Under system holdout, the model should beat this without losing coverage; composition-holdout results diagnose interpolation. |
| Raw observed-pair frequency (new direct control) | Does low-rank completion add information beyond direct pair memorisation? | Training formulas only; score candidate pair `(a,b)` by the same `log1p(C_ab)/log1p(T)` target used by the factor model. Zero for unseen pairs. | Count pairs only. | O(T + N + N log N); 117×117 counts. | On system holdout every held-out pair should be unseen and tied at zero; improvement over this control isolates cross-pair factor generalisation. On composition holdout it tests whether factorisation beats raw frequency. |
| Observed-pairs-only factor ablation (new, conditional) | Are results driven by treating missing pairs as weak zero targets? | Identical training formulas, rank, regularisation, initialisation and optimizer; set missing-pair weight to zero and still score all candidates. | Yes, independently per split. | Same asymptotic fit cost as the main model. | Similar conclusions across the frozen grid support robustness to the PU assumption; material changes show the assumption is load-bearing and must temper claims. |

Do not ablate the oxygen-ternary scope or system filter: those define the population,
not optional features. Treat the three mixed-label policies as label sensitivity,
not model ablations. Defer rank sweeps; a sweep would be model selection or
stability analysis and needs its own prospective ranks, restarts and consensus
rule. The direct pair-frequency control is more informative first.

## E. PyTorch decision

**Decision: defer.**

The current learned problem has only 117 element rows and rank four. Reimplementing
the same weighted symmetric factor objective in PyTorch would mainly compare an
optimizer/autodiff stack with Julia's explicit projected-gradient implementation;
it would not add a scientifically distinct predictor. The measured primary run
spent about 18.71 seconds fitting all 120 branches and 0.83 seconds ranking them,
so accelerator support is not needed. A neural collaborative-filtering scorer or
MLP would require a new representation and a defensible PU loss/negative-sampling
policy. Adding one merely to claim PyTorch would be disconnected from the current
evidence.

Reconsider PyTorch only after both of these prerequisites hold:

1. the system-aware evaluation and raw-pair control identify a specific remaining
   error mode, such as inability to order stoichiometries within a system; and
2. a representation with information capable of addressing that error is available
   without test leakage—for example training-only composition descriptors or
   structure/property features with complete provenance.

The smallest credible later experiment would keep the exact outer splits,
candidate universe, held-out positives, filters, tie policy and metric code. It
would use one shallow model over the agreed representation, a prospectively
defined PU objective, training-only negative/unlabelled sampling, deterministic
CPU execution first, fixed seeds, inner grouped validation for early stopping and
hyperparameters, and TSV rankings plus TOML/JSON provenance consumable by Julia
and the independent Python validator. GPU use would require recording device,
driver, framework determinism settings and nondeterministic operators. Until the
loss and representation are scientifically specified, optimizer, learning rate,
regularisation and negative-sampling counts should not be invented.

## F. Proposed architecture and algorithmic analysis

Let `L` be formula-string length, `a` distinct elements per composition, `R` source
records, `G` canonical groups, `T` training compositions, `N` candidates, `E`
element vocabulary size (117 non-O elements in the pair model), `r` factor rank,
`I` accepted optimizer iterations and `B≤60` line-search attempts.

| Path and implementation | Current data structures | Time | Working memory and allocations |
| --- | --- | --- | --- |
| `Composition` parsing | Regex matches, `Dict{String,Int}`, sorted tuple of `Pair{String,Int}`, canonical `String` | O(L + a log a), treating the fixed 118-symbol validity scan as constant | O(a + L) per composition; strings and pair vectors are allocated before the immutable tuple/string. |
| SQLite query and rank | SQLite row iterator, `Vector{Tuple{Composition,Float64}}`, ranking-value vector and `sortperm` | O(Rq·parse + N log N), where `Rq` is rows returned/scanned by the adapter | O(N) Julia result/order storage. Standard tables apply element/arity filters after parsing; legacy tables push element predicates into SQL. |
| Generic `rank!` | score `Vector{Float64}`, permutation vector | O(N·S + N log N), `S` scorer cost | O(N); `permute!` reorders in place after the value/order arrays are built. |
| PU popularity/random | `Dict{String,Int}`, per-candidate named tuples and SHA strings, sorted vector | O(Ta + Na + N log N) | O(N + E); SHA strings dominate current per-candidate allocations. |
| PU maximum similarity | `Vector{PUVector}` for training, one candidate vector at a time, score vector | O(NTa² + N log N); `a=3` in scope | O(Ta + N), not O(NT); no pairwise score matrix is materialised. |
| MP audit | complete TSV/JSON byte arrays, JSON row vector, TSV row vector, `Dict{Composition,Vector{NamedTuple}}`, output group vector | O(R·parse + R log within-group + G log G) | O(input bytes + R + G). Unlike `validate_database`, this audit is not streaming end to end. |
| SQLite full validation | DB row iterator, bounded issue vectors and count dictionaries | O(R·parse) plus SQLite integrity check | O(max_issues + tables/categories) in Julia, excluding SQLite/page cache. |
| TSV/database ingestion | row generator, SQLite transaction/statements and SHA context; indexed duplicate lookup | Approximately O(R log R) with the formula B-tree and inserts | Streaming in Julia; database and indexes are on disk. Publication uses a no-clobber hard link. |
| Pair feature construction | sorted composition vector, dense `Matrix{Int}` counts, dense `Matrix{Float64}` target, `BitVector` | O(T log T + Ta + E²) | O(T + E²). |
| Pair-model fit | dense factor matrix, target/weight/count matrices, gradient and temporary factor/delta arrays | O(I·B̄·E²r), where `B̄` is actual line-search evaluations | O(E² + Er) peak working state, but repeated broadcast temporaries cause much larger cumulative allocation. Trace is O(I). |
| Pair-model scoring/ranking | candidate named tuples, factor dot products, SHA tie strings, sort | O(Nr + N log N) | O(N + Er). |

Deterministic ordering matters because cutoffs often intersect large exact-score
ties. Input order, process hash randomisation or a different sort implementation
would otherwise change Hits@K without changing the model. The versioned SHA keys
make split selection, random rankings and ties reproducible across input permutations
and supported processes; canonical formula is a final collision fallback.

### F.1 Existing empirical evidence

- The 12-row fixture measurement reduced first in-process query latency from about
  142 ms to 6 ms after representative precompilation; warm-query differences were
  too small to interpret. This is startup evidence, not an algorithmic speedup.
- A production legacy query returned 1,108 rows in roughly 104–106 ms warm. A
  streaming validation scan of 4,736,551 rows took about 39 seconds in one
  exploratory run.
- The synthetic real-size similarity benchmark scored about 35.2 million
  candidate/training pairs in 0.132 s and allocated 3.2 MiB; full `pu_rank`
  similarity took 0.141 s and 21.8 MiB. A stored Float64 pairwise matrix would be
  268.9 MiB. These are cumulative allocations, not peak RSS.
- In the retained real pilot, similarity ranking totaled about 2.90 s across 20
  splits, versus 0.45 s for popularity and 0.37 s for random, including first-call
  compilation effects.
- The 120 primary pair fits totaled 18.71 s; ranking totaled 0.83 s. Mean cumulative
  fit allocation was about 75 MiB for composition branches and 72 MiB for system
  branches. Input verification, output, analysis, startup and reproduction were
  not included in those totals.

### F.2 Next benchmark design

Create a separate `benchmark/Project.toml` with BenchmarkTools so benchmarking
dependencies do not enter the package runtime. Add:

- microbenchmarks for parsing, tie-key construction, `pu_metrics`, raw pair score,
  factor objective/gradient and sorting at controlled tie rates;
- scaling benchmarks for `N`, `T`, `E` and `r`, reporting median time, allocations
  and fitted slopes against the theoretical terms;
- end-to-end phase timers for verify/audit, split construction, fitting, scoring,
  sorting, metric computation and output;
- OS-reported peak RSS in a fresh process when making memory claims;
- machine, OS/architecture, Julia, dependency, thread-count, dataset hash and
  commit/dirty-state metadata.

Profile before optimizing. Likely targets are SHA string allocation in ranking,
MP audit's full-file duplication and broadcast temporaries in projected gradient,
but none should be called a bottleneck until a profiler on the intended workload
shows it.

Defensible claims after the proposed measurements include “streamed maximum
similarity with O(T+N) working storage,” “deterministic O(N log N) ranking,” and a
specific measured reduction in time/allocations on a named workload. Do not claim
generic “faster ranking,” lower peak memory from `@allocated`, production-scale
speedup from the 12-row fixture, or asymptotic improvement from a constant-factor
change.

### F.3 Repository integration

Preserve every frozen protocol file and existing result bundle. Prefer additive
files and a new protocol ID.

```text
src/
  ranking_evaluation.jl       reusable experimental relevance/system metrics
  pair_frequency_model.jl     direct observed-pair control
  evaluation_suite.jl         new Research orchestration, no CLI change initially
benchmark/
  Project.toml                isolated BenchmarkTools environment
  ranking_scaling.jl          controlled N/T/tie-rate scaling
  factor_scaling.jl           E/r/iteration and allocation scaling
scripts/
  run_evaluation_suite.jl     one explicit frozen-suite entry point
  analyze_evaluation_suite.py independent reconstruction and reporting
docs/
  evaluation-roadmap.md       this plan
  evaluation-metrics.md       reusable metric semantics and schemas
  mp-evaluation-suite-v3.md   new pinned prospective real-data protocol
test/
  test_ranking_evaluation.jl
  test_pair_frequency_model.jl
  test_evaluation_suite.jl
  test_evaluation_analysis.py
reports/local/
  mp-evaluation-suite-v3-*/   ignored memberships, rankings, factors and results
```

Reusable package code should calculate metrics and scores from in-memory canonical
objects. Research orchestration should verify sources, rebuild split-local state,
write complete artifacts and refuse overwrite. Python should independently read
the saved schema and recompute results; it should not call Julia metric code.
Plots and narrative tables belong to generated analysis output, not `src/`.
Notebooks are unnecessary for the core workflow.

Avoid modifying fields in existing schema-v1 reports. Define a new result schema
with, at minimum:

- dataset ID/version/retrieval metadata and hashes;
- audit/preprocessing algorithm and implementation hashes;
- code commit, dirty flag, patch/source-tree digest and relevant file hashes;
- protocol ID/hash, split algorithm, split membership hashes and label policy;
- candidate-generation/filter definition and exclusion counts;
- method/baseline/ablation configuration, seed roles and coverage policy;
- metric algorithm/version, K values, grouping rule and denominator counts;
- Julia/Python versions, dependency locks, OS, architecture, CPU, threads and
  optional accelerator details;
- hashes for every deterministic output, with runtime/host measurements clearly
  separated.

A deterministic run ID can be the SHA-256 of the canonical scientific configuration
and input identities. Wall-clock timestamps and output paths must not enter that
identity.

## G. Implementation sequence

### Milestone 1 — Reusable metric kernel and system diagnostics

**Status:** implemented 14 September 2026 as the additive experimental
`recovery_metrics` API with a metric contract and independent Julia/Python
hand-worked checks. Existing frozen reports and `pu_metrics` were not changed.

- **Objective:** extract a rigorously specified evaluation kernel without changing
  any frozen result. Implement composition Hits/Recall/enrichment, optional binary
  NDCG, distinct/system recall and effective-system diagnostics.
- **Likely changes:** `src/EkaCompositions.jl`, `docs/api-stability.md`,
  `test/runtests.jl`; do not edit frozen protocols.
- **New files:** `src/ranking_evaluation.jl`, `docs/evaluation-metrics.md`,
  `test/test_ranking_evaluation.jl`, `test/test_evaluation_metrics.py`.
- **Tests:** hand-worked rankings; no hits/full hits; ties at and across K; duplicate
  canonical candidates; missing relevance; empty relevance; K>N; K=N; input-order
  invariance; system grouping; one system with many stoichiometries; exact Julia/
  Python agreement; no mutation.
- **Expected output:** a versioned in-memory metrics object and deterministic TSV/
  JSON row schema, exercised only on synthetic fixtures and existing saved rankings.
- **Dependencies:** none beyond current Julia/Python standard libraries.
- **Scientific question answered:** are current conclusions robust when recovery
  concentration across chemical systems is made visible?

Milestones 2 and 3 are now complete. The next implementation milestone is
Milestone 4, the prospective v3 protocol freeze and missing-pair ablation.

### Milestone 2 — Uniform provenance and result schema

**Status:** implemented 22 September 2026 as the internal schema-v1
`EvaluationSuite` writer/validator and `docs/evaluation-bundle-schema.md`. It has
only synthetic coverage; no frozen report reader or existing result was changed.

- **Objective:** make a result independently traceable and restorable without
  experiment-specific knowledge.
- **Likely changes:** research writers and validation utilities only; preserve old
  readers and schema-v1 bundles.
- **New files:** `src/evaluation_suite.jl`, a schema document and synthetic golden
  bundle under `test/fixtures/` if small enough.
- **Tests:** schema validation; missing/extra/wrong-typed keys; source, split,
  config and output tampering even after internal checksum rewrite; clean and dirty
  tree identities; fixed-seed rerun; runtime excluded from deterministic equality;
  no overwrite and partial-output cleanup.
- **Expected output:** one `run.toml`, complete `metrics.tsv`, rankings and a
  deterministic inventory with explicit environment metadata.
- **Dependencies:** Milestone 1.
- **Scientific question answered:** can an evaluator establish exactly which data,
  code, split, metric and configuration produced a number?

### Milestone 3 — Direct pair-frequency control

**Status:** implemented 22 September 2026 as the internal
`PairFrequencyModel`. Its synthetic suite coverage verifies the direct target,
training/candidate isolation, system-holdout zero-score property and deterministic
ties. No real result has been run.

- **Objective:** formalise the unfactorised target matrix as a baseline.
- **Likely changes:** the new suite only; leave `src/element_pair_model.jl` and prior
  evidence unchanged.
- **New files:** `src/pair_frequency_model.jl`,
  `test/test_pair_frequency_model.jl`.
- **Tests:** hand-counted pairs; canonical duplicate rejection; permutation
  invariance; same-system stoichiometry ties; unseen-pair zero; system-holdout
  all-zero property; candidate/label isolation; deterministic cutoff ties.
- **Expected output:** complete rankings and coverage/tie diagnostics on synthetic
  splits.
- **Dependencies:** Milestones 1–2.
- **Scientific question answered:** does low-rank factorisation add cross-pair
  generalisation beyond direct observed-pair frequency?

### Milestone 4 — Freeze v3 protocol and missing-pair ablation

- **Objective:** prospectively define the real comparison before inspecting any
  new result. Specify system holdout primary, composition control, all carried
  label policies, raw pair frequency, the main converged/fixed-compute model and
  the alpha=0 ablation.
- **Likely changes:** add a new protocol pin in `src/mp_recovery.jl`; never edit an
  old protocol or reuse an old ID.
- **New files:** `docs/mp-evaluation-suite-v3.md`,
  `test/test_evaluation_suite.jl` and `scripts/run_evaluation_suite.jl`.
- **Tests:** training-only preprocessing, outer membership equality with v2,
  split-local fitting, alpha-only configuration difference, complete candidate
  coverage, common-candidate score invariance, and frozen grid completeness.
- **Expected output:** signed-off protocol bytes/hash, synthetic preflight and a
  no-results design freeze.
- **Dependencies:** Milestones 1–3 and a decision on whether primary optimisation
  means convergence or an explicitly fixed compute budget.
- **Scientific question answered:** is the next real run capable of separating
  marginal frequency, direct pair memory, low-rank generalisation and the weak-zero
  assumption fairly?

### Milestone 5 — Execute, independently validate and report

- **Objective:** run the frozen suite once on the retained snapshot, preserving all
  favorable and unfavorable branches.
- **Likely changes:** no scientific code after freeze except a separately versioned
  correctness fix with affected reruns.
- **New files:** `scripts/analyze_evaluation_suite.py`; local ignored result and
  analysis directories; an attributed aggregate tracked summary only after review.
- **Tests:** Python reconstruction of metrics, raw pair scores, ranking order,
  system diagnostics, factors/objective where applicable and schema/inventory;
  complete same-environment rerun comparison.
- **Expected output:** per-split rankings/metrics, macro summaries, system-aware
  concentration results, runtimes and explicit negative-result retention.
- **Dependencies:** Milestone 4 freeze and artifact-specific sharing review.
- **Scientific question answered:** does the element-pair model add robust value
  under unseen-system recovery, and is that value dependent on missing-pair
  penalisation or clustered stoichiometric hits?

### Milestone 6 — Reproducible performance characterization

- **Objective:** connect theoretical complexity to measured phase costs and only
  then optimize a demonstrated bottleneck.
- **Likely changes:** performance-sensitive implementation only after baseline
  capture; scientific ranking order must remain byte-identical.
- **New files:** isolated `benchmark/` environment/scripts and a benchmark report.
- **Tests:** golden ranking digests before/after, allocation ceilings where stable,
  and scaling fixtures separated from correctness tests.
- **Expected output:** raw benchmark data, environment metadata, profiles and a
  before/after comparison for any accepted optimization.
- **Dependencies:** stable Milestone 1 API/schema.
- **Scientific question answered:** what actually limits scaling, and which runtime/
  memory claims are supported?

### Milestone 7 — PyTorch gate, not implementation by default

- **Objective:** decide whether a new representation and PU objective answer a
  remaining scientific question.
- **Likely changes/new files:** a feasibility document first; no dependency until
  the gate is positive.
- **Tests/output:** if approved later, deterministic synthetic gradient/loss checks,
  negative-sampler isolation, CPU reproducibility, shared-split schema compliance
  and Julia/Python metric agreement.
- **Dependencies:** Milestone 5 error analysis and appropriate feature provenance.
- **Scientific question answered:** would nonlinearity or a richer representation,
  rather than merely a different optimizer, improve the same recovery task?

## H. Benchmark matrix

The following is the recommended scientific grid. “20 splits” means descriptive
overlapping holdouts; it is not 20 independent datasets. Every row uses K = 100
primary and K = 20, 50, 200 secondary, with Hits, Recall, enrichment and system
diagnostics from the same complete ranking.

| Method | Split | Policies | Seed/repetition | Runtime class | Purpose |
| --- | --- | --- | --- | --- | --- |
| Analytical uniform random + deterministic hash realization | System primary; composition control | original, exclude mixed, unlabel mixed | 20 split seeds; one declared ranking seed each | Very low | Calibrate prevalence and tie-independent chance behavior. |
| Element popularity | System primary; composition control | all three | Deterministic per split | Low | Test against marginal historical element frequency. |
| Maximum composition cosine | System primary; composition control | all three | Deterministic per split | Medium, O(NT) comparisons | Diagnose dependence on near stoichiometric analogues. |
| Raw pair frequency | System primary; composition control | all three | Deterministic per split | Low | Separate direct pair memory from low-rank completion. |
| Rank-4 element-pair model, prospectively chosen convergence/compute rule | System primary; composition control | all three | Fixed initialization; independently refit per split | Medium | Main learned association comparator. |
| Rank-4 alpha=0 ablation | System primary; composition control | all three | Same initialization and fit rule | Medium | Test dependence on weak-zero missing-pair loss. |
| Optional leave-element-out stress test, all simple methods first | Element cold-start | policy chosen prospectively | One split per adequately supported element or fixed declared subset | Medium | Expose transfer limits for unseen elements; not a leaderboard extension. |

Do not repeat deterministic models under arbitrary “evaluation seeds.” If
initialisation sensitivity becomes a question, predeclare multiple initialisation
seeds and report all of them as a separate stability experiment rather than
selecting the best restart.

### H.1 Required cross-cutting tests

#### Metrics

- Hand-compute Hits, Recall, observed-label fraction, enrichment, DCG/NDCG,
  distinct hit systems, system recall and effective systems.
- Cover K=1, K=N, K>N, unsorted K input and duplicate K.
- Reject empty candidate rankings, duplicate canonical candidates, duplicate
  relevance, relevance outside the candidate universe and empty relevance unless
  a future API explicitly defines nullable denominators. Preserve `pu_metrics`'s
  current strict behavior for compatibility.
- Test all-zero relevance scores, all-relevant rankings, no top-K hits and ties
  spanning K.
- Verify metric values do not depend on candidate input order once a ranking is
  supplied, and that metric computation does not mutate inputs.
- Compare Julia with an independent Python implementation on golden fixtures;
  include integer/rational expected-random values to avoid floating ambiguity.

#### Splits and leakage

- Assert train/candidate composition disjointness and, for the primary protocol,
  train/candidate chemical-system disjointness.
- Include proportional formulas, symbol permutations, polymorph records, mixed
  flags, unlabelled-only systems, unsupported records and unequal system sizes.
- Assert deterministic membership under input and seed-list permutation.
- Change evaluator labels and unrelated candidate membership while holding
  training fixed; fitted state and shared-candidate scores must not change.
- If inner validation is introduced, assert outer candidates never appear in
  inner training, preprocessing, sampling or selection.

#### Baselines and ablation

- Check popularity and pair counts on hand-worked examples.
- Prove raw pair frequency is zero for every candidate in a valid system holdout.
- Verify maximum similarity against direct pairwise `similarity` and a Python
  calculation on a small fixture.
- Verify alpha=0 changes only the missing-pair weights/configuration; observed
  targets, regularisation, initialization, stopping rule and membership must match.
- Test complete finite score coverage and explicit cold/unseen states.

#### Ranking and reproducibility

- Golden-test split, random and tie SHA keys, including exact-score tie blocks at
  K and synthetic hash-collision fallback logic where feasible.
- Reject duplicate candidates rather than silently retaining one.
- Re-run with reversed inputs and perturbed global RNG state.
- Validate result schema types, required fields, deterministic run ID and every
  output checksum; reject semantically corrupted membership/results even after
  checksums are rewritten.
- Compare two same-environment synthetic runs byte for byte except declared
  runtime/host fields.

#### Performance

- Keep correctness fixtures small. Put realistic scaling and allocation checks in
  the isolated benchmark suite, not the unit suite.
- Record compilation-inclusive and warmed measurements separately.
- Use a fresh process for peak RSS and end-to-end latency.
- Verify any optimization preserves complete ranking digests, not only top K.

## I. Risks and open questions

1. **Scientific target:** Is the goal database completion, unseen-system transfer
   or actual experimental recommendation? The current data answer only the first
   two, using a provenance proxy.
2. **Candidate universe:** There is no enumerator for absent formulas. Ranking
   already catalogued MP compositions cannot measure prospective discovery among
   genuinely unknown candidates.
3. **Ground truth:** `theoretical=false` is not literature-audited synthesis
   success; mixed groups show label ambiguity. Unlabelled is not failure.
4. **Within-system dependence:** The main model ignores stoichiometry and generates
   very large tie blocks. Composition hits can be concentrated in a few systems.
5. **Optimisation:** The frozen primary model often stopped at its iteration cap.
   A future protocol must choose convergence handling before results, not promote
   the favorable checkpoint afterward.
6. **Split dependence:** The 20 hash holdouts overlap. They quantify sensitivity
   to membership but do not create independent experimental replicates.
7. **Cross-design confounding:** Existing system and composition pools differ in
   training size, candidate size and prevalence. Without a prospectively defined
   matched control, protocol differences are descriptive, not causal effects of
   chemical separation.
8. **Chemical OOD:** System disjointness does not prevent close periodic-family
   analogues. A family split needs an external, justified taxonomy.
9. **Time:** The snapshot has retrieval time but no defensible first-observation
   time. Chronological evaluation is currently unavailable.
10. **Distribution and reproducibility:** Aggregate attributed results may be
    shareable, but exact public reruns still depend on local record-level artifacts
    and final permissions review.

## J. CV / README claims unlocked

Claims should be tied to completed evidence, not planned work.

| Completed milestone | Defensible claim | Claims still not supported |
| --- | --- | --- |
| Existing repository | “Implemented deterministic positive–unlabelled composition-recovery benchmarks with composition-safe and chemical-system-grouped holdouts.” | Prospective discovery, synthesis success, independent replicates. |
| Existing repository | “Benchmarked element popularity, maximum composition similarity and a nonnegative element-pair factor model on identical candidate pools with independent Python validation.” | Superiority to published state of the art or reproduction of Seko. |
| Milestone 1 | “Implemented reproducible fixed-budget recovery and system-aware ranking diagnostics with Julia/Python cross-checks.” | Chemically meaningful diversity unless a chemistry-aware definition is added. |
| Milestones 2–3 | “Added a traceable result schema and an unfactorised pair-frequency control to isolate low-rank generalisation.” | Model value until the frozen real comparison is complete. |
| Milestones 4–5 | “Evaluated a nonnegative element-pair model and missing-pair ablation under leakage-resistant unseen-system recovery, reporting every split and label policy.” | General materials discovery or causal effect of system separation. |
| Milestone 6 | “Profiled the ranking pipeline and reduced [named phase] runtime/allocations by [measured amount] on [named workload] while preserving ranking digests.” | Generic speed or peak-memory claims without the corresponding measurements. |
| Milestone 7, only if approved and completed | “Compared Julia and PyTorch models under identical splits, candidates, filters and metric implementations.” | A PyTorch claim merely because a toy network exists; superiority without a prospectively controlled result. |

The existing README can already credibly claim reproducible ranking evaluation,
leakage-resistant grouped evaluation, baseline comparisons, label sensitivity,
algorithmic determinism and same-platform exact reruns. It should not claim an
“ablation study of element-pair interactions” until the raw pair control and/or
missing-pair ablation is executed under a new protocol.

## Final direction

The best next investment is not a larger model. It is a small evaluation kernel
that makes system-level concentration impossible to overlook, followed by the raw
pair-frequency control. If those results show that the factor model's apparent
system-holdout advantage survives system-aware evaluation and truly comes from
low-rank cross-pair generalisation, a richer stoichiometric model becomes a
well-posed next question. If they do not, the negative result is scientifically
more valuable than adding PyTorch or tuning rank until one branch improves.
