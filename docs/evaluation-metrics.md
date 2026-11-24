# Ranking evaluation metric contract

`recovery_metrics` is the reusable experimental metric kernel proposed in the
[evaluation roadmap](evaluation-roadmap.md). It evaluates an already ordered
candidate pool; it does not construct a split, score candidates or attach a
scientific meaning to labels.

## Inputs and unit of evaluation

```julia
using EkaCompositions

ranking = ["LiNaO", "Li2NaO", "CaTiO3", "MgAl2O4"]
relevant = ["LiNaO", "Li2NaO", "MgAl2O4"]
rows = recovery_metrics(ranking, relevant;
    budgets=[1, 2, 4], scores=[0.9, 0.9, 0.8, 0.1])
```

`ranking` is a complete, ordered collection of unique formula strings or
`Composition` values. `relevant` is a nonempty unique subset. Canonically
equivalent spellings are duplicates. `budgets` are unique positive integers no
larger than the candidate count; output rows are sorted by budget.

The natural unit is one ranking/candidate pool, such as one outer recovery split.
Metrics can be macro-averaged across splits later. The function deliberately does
not pool splits, because overlapping holdouts are not independent datasets and
pooling would weight larger relevant sets more heavily.

An optional `scores` collection enables cutoff-tie diagnostics. Scores must be
finite real values aligned with the complete ranking and sorted descending. Ties
use exact Float64 equality: evaluation never rounds scores or changes order.

## Composition-level fields

For a cutoff `K`, candidate count `N`, relevant set `R` and hits `H_K`:

| Field | Definition |
| --- | --- |
| `hits` | `H_K`, relevant compositions in the first K |
| `observed_label_fraction` | `H_K / K`; not a synthesis-success rate |
| `recall` | `H_K / |R|`, recovery of deliberately held-out positives |
| `enrichment` | `(H_K / K) / (|R| / N)` |
| `random_expected_hits` | `K|R|/N` under uniform selection without replacement |
| `random_expected_hits_numerator`, `random_expected_hits_denominator` | Exact reduced fraction for the same expectation |
| `dcg` | Sum of `1/log2(rank+1)` for relevant items at ranks at most K |
| `ndcg` | Binary DCG divided by the ideal DCG for `min(K, |R|)` early hits |

Binary NDCG is a position-sensitive diagnostic, not a replacement for Hits@K.
Every field treats the supplied relevance set as evaluator ground truth. In a PU
experiment, unlabelled candidates can still be scientifically viable, so none of
these fields is precision over confirmed negatives.

## System-concentration fields

A chemical system is the unordered set of elements in a composition, ignoring
stoichiometry. `LiNaO` and `Li2NaO` are distinct compositions in one system.

| Field | Definition |
| --- | --- |
| `selected_system_count` | Distinct systems represented in the first K |
| `relevant_system_count` | Distinct systems represented by the complete relevant set |
| `hit_system_count` | Relevant systems with at least one composition hit by K |
| `system_recall` | `hit_system_count / relevant_system_count` |
| `effective_hit_systems` | `H_K² / sum_s h_s²`, where `h_s` is the hit count in system s |
| `largest_hit_system_fraction` | Largest `h_s / H_K`, or zero when there are no hits |

The effective count is one when every hit comes from one system and reaches the
ordinary hit-system count when hits are distributed evenly. These are clustering
diagnostics. They do not claim that element-set diversity equals chemical,
structural or functional diversity.

## Cutoff ties

When scores are supplied, each row also reports:

- `cutoff_score`;
- `cutoff_tie_size` across the complete ranking;
- `cutoff_tie_selected` in the first K; and
- `cutoff_tie_crosses`, which is true when only part of the exact-score tie block
  is selected.

The metric function preserves the supplied order. The ranking producer remains
responsible for a deterministic, score-independent tie rule. PU experiments use
the versioned SHA-256 tie key and canonical formula fallback defined by their
protocol.

## Failure behavior and compatibility

Empty rankings/relevance, duplicate canonical formulas, relevance outside the
ranking, invalid budgets, nonfinite or misaligned scores and scores that are not
descending are errors. Inputs are not mutated.

This API is additive and experimental. It does not change `pu_metrics`, the v1
PU CLI or any frozen output schema. Existing frozen protocol documents and result
bundles remain unchanged.
