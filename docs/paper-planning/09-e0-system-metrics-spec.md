# E0 — Matched system-metric analysis specification

Written 22 September 2026, before any all-method system metric was computed. **Post hoc:** every primary ranking already exists, and the pair-model concentration diagnostic (C7) had already been inspected. This analysis re-reads saved rankings; it does not refit, re-rank, re-split or relabel anything. Its SHA-256 is recorded by the analyzer, which binds the specification used but does not prove when it was written.

## Question

In the saved evaluations, does the pair model's composition-level Hits@100 advantage over training-element popularity (C5) also reach more **distinct positive chemical systems**? Or is it concentrated in fewer systems than the reference methods?

## Fixed grid

- **Methods (4):** `random`, `popularity`, `similarity` from `mp-system-holdout-v2-2026-08-31/results/{design}/{policy}/split-NN/{method}.tsv`; `element_pair` from `element-pair-evaluation-2026-08-31/results/{design}/{policy}/split-NN/ranking.tsv` (2,000-iteration primary fits only; the 20k stability run is excluded).
- **Branches (6):** designs `composition` and `system` × policies `original`, `exclude_mixed` and `unlabel_mixed`.
- **Splits (20):** seeds 0–19. **Budgets (4):** K = 20, 50, 100 and 200.
- **Total:** 4 × 6 × 20 × 4 = 1,920 rows. A missing, extra or duplicated row is an error.

## Inputs and validation (errors, not warnings)

1. Every file read must match its SHA-256 in its own bundle's `results/config.toml` `deterministic_file_hashes`.
2. The pair bundle's `baseline/{design}/{policy}/split-NN` memberships must hash-equal the v2 bundle's membership files for the same branch and split.
3. Each ranking is a permutation of `inputs/candidates.tsv`, with ranks 1..N. Each row's `observed_label` equals `evaluation/labels.tsv`. The relevant set R equals `evaluation/heldout.tsv`, which equals the positive-labelled candidates.
4. Recomputed Hits@K, N and |R| equal the saved `metrics.tsv` value for every one of the 1,920 rows.

## Metrics per row

Definitions follow `docs/evaluation-metrics.md`. A system is the unordered element set of a canonical formula, with stoichiometry ignored. Let R_S be the systems of R and h_s the number of hits from system s in the first K.

| Field | Definition |
| --- | --- |
| `hits` | Composition hits in the first K, cross-checked against saved metrics |
| `selected_system_count` | Distinct systems in the first K |
| `relevant_system_count` | \|R_S\|, shared by all methods within a branch and split |
| `hit_system_count` | Systems with h_s ≥ 1 |
| `system_recall` | `hit_system_count / relevant_system_count` |
| `effective_hit_systems` | H²/Σh_s², or 0 when H = 0. Concentration index, not a sample size |
| `largest_hit_system_fraction` | max h_s / H, or 0 when H = 0 |
| `random_expected_hit_systems` | Exact uniform-random reference Σ_s [1 − C(N−r_s, K)/C(N, K)], where r_s = \|R ∩ s\| |

**Tie reporting**, for score-bearing methods only; `random` has no score and gets NA. Exact Float64 equality on the saved score strings gives `cutoff_score`, `cutoff_tie_size`, `cutoff_tie_selected` and `cutoff_tie_crosses`. When a tie crosses the cutoff, the Hits@K achievable under any reordering of that tie block is reported as `hits_tie_min` and `hits_tie_max`, with its expectation under a uniformly random tie order as `hits_tie_expected`. The saved order, which uses the protocol's SHA-256 tie key, remains the reported result. System metrics are not recomputed under alternative tie orders.

## Summaries and primary contrast

For each method, branch and budget: means over 20 splits of every field above (macro-averaged per split, never pooled), plus the number of splits whose cutoff tie crosses. Paired within-split differences against `popularity` for `random`, `similarity` and `element_pair` on `hits`, `hit_system_count`, `system_recall` and `effective_hit_systems`: mean, median, min, max and positive/zero/negative split counts. No p-values, confidence intervals or pooled significance tests.

**Primary contrast (stated before computing):** system design, K = 100, `element_pair − popularity` on `hit_system_count`, separately for each of the three policies. Descriptive reading rule:

- **Extends:** the mean difference is > 0 and positive splits outnumber negative splits in all three policies.
- **Mixed:** this holds in one or two policies.
- **Does not extend:** it holds in none. This is a valid result, and it is retained and reported with the same prominence as the other two.

All other budgets, designs, contrasts and fields are secondary and are reported in full, whichever way they point. The reading rule is not changed after seeing the numbers.

## Independent computation

A standard-library Python analyzer computes every field. The dirty-tree Julia `recovery_metrics` computes the same rows from the same files. All shared fields must agree: exactly for integers and ties, and within 1e-12 for floats. A mismatch is a failure. At least two rows are hand-worked in the results note: one system-design pair-model row and one composition-design reference row.

## Out of scope

No new rankings, fits, seeds, budgets, tie rules, label policies, candidate pools or significance testing. No claim that element-set coverage equals chemical, structural or functional diversity. No claim about synthesis or discovery.
