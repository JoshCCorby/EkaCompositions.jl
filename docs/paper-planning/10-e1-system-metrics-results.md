# E1 — Matched system metrics: results

Completed 22 September 2026 under the [E0 specification](09-e0-system-metrics-spec.md), SHA-256 `d6fb6add…a9a83f`. **Post hoc.** The analysis re-reads saved rankings only: nothing was refit, re-ranked, re-split or relabelled, and nothing new was queried from MP. All numbers are descriptive macro-averages over 20 overlapping holdouts. None of them is an inferential estimate.

## Validation

| Check | Result |
| --- | --- |
| Input identity | 842 files, comprising 480 rankings, 360 membership files and 2 metric tables, each matched to its bundle's `config.toml` inventory. Pair-bundle memberships hash-equal the v2 memberships for all 120 branch/splits. |
| Grid | 1,920 rows, covering 4 methods × 6 branches × 20 splits × 4 budgets, with none missing or duplicated |
| Saved metrics | Recomputed Hits@K, N and \|R\| equal the saved `metrics.tsv` value for all 1,920 rows |
| Julia cross-check | The `recovery_metrics` kernel (`src/ranking_evaluation.jl` `1db284b6…`) agrees with the independent Python analyzer on every shared field. Maximum float difference is 0.0. |
| Prior diagnostic | Reproduces all 60 rows of the v0.1.1 pair-model `system-concentration-by-split.tsv` |
| Hand-worked rows | See below; both agree exactly |

**Hand-worked rows.** The per-system hit counts below came from `awk` over the ranking files, independently of both analyzers.

- *System/original/split 0/element_pair/K=100:* h_s = 17, 9, 7, 6, 4, 4, 4, 1. So H = 52, with 8 hit systems out of 361 relevant and 15 selected systems. Σh_s² = 504, so effective hit systems = 2704/504 = 5.365 and largest share = 17/52 = 0.327.
- *Composition/original/split 0/popularity/K=20:* h_s = 4, 2, 2. So H = 8, with 3 hit systems out of 769 relevant and 4 selected systems. Effective hit systems = 64/24 = 2.667 and largest share = 0.5.

## Primary contrast (stated before computing)

System design, K=100, `element_pair − popularity` in positive hit systems:

| Policy | Mean Δ | Median | Range | +/0/− splits | Meets rule |
| --- | ---: | ---: | ---: | ---: | :---: |
| original | +2.80 | +2.0 | −3 to +8 | 16/3/1 | yes |
| exclude_mixed | +1.15 | +1.0 | −2 to +4 | 13/3/4 | yes |
| unlabel_mixed | +1.25 | +1.0 | −3 to +7 | 14/0/6 | yes |

**Reading under the pre-stated rule: "extends".** Relative to popularity, the pair model's system-holdout Hits@100 advantage comes with slightly more positive systems, not fewer, under all three policies. The margins are 1–3 systems out of roughly 325–362 relevant systems. Three secondary results qualify this reading and must accompany it.

## Secondary results that change the interpretation

**1. In system holdout, both system-level scorers reach far fewer systems than random selection or similarity.** In composition holdout the gap is smaller and not uniform: under the exclude policy, popularity roughly matches random. Mean values at K=100:

| Design / policy | Relevant systems | Random expected hit systems | Random | Popularity | Similarity | Pair |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| composition / original | 759.25 | 12.97 | 11.50 | 5.65 | 12.15 | 6.60 |
| composition / exclude | 612.80 | 10.06 | 9.05 | 9.35 | 16.30 | 6.75 |
| composition / unlabel | 612.80 | 8.61 | 7.85 | 7.05 | 12.85 | 5.65 |
| system / original | 362.15 | 39.42 | 40.15 | 6.20 | 23.75 | 9.00 |
| system / exclude | 324.60 | 33.49 | 33.85 | 9.95 | 21.60 | 11.10 |
| system / unlabel | 324.60 | 30.13 | 31.00 | 8.65 | 20.15 | 9.90 |

The positive-hit-system columns are realized values. For comparison, the Hits@100 values for system/original are random 43.35, popularity 44.30, similarity 29.85 and pair 52.25. The pair model's top 100 spans a mean of 13.5 systems, against 82.6 for random and 58.3 for similarity. Popularity and the pair model score every composition in a system identically. So at a fixed K they tend to fill the list with whole systems.

In system holdout, similarity has fewer composition hits than popularity in 19 of 20 splits under every policy. But it reaches more positive systems in all 20 splits under every policy: +17.55, +11.65 and +11.50 mean. Composition-level Hits@K and system coverage therefore **rank the methods differently**. The pair−similarity difference in hit systems is about −14.75 under the original policy. This is a difference of means; the paired contrast was not tabulated.

**2. The alternative-policy margins over popularity depend on the budget.** System design, pair − popularity hit systems, mean (+/0/−):

| Policy | K=20 | K=50 | K=100 | K=200 |
| --- | ---: | ---: | ---: | ---: |
| original | +0.35 (8/6/6) | +1.60 (14/4/2) | +2.80 (16/3/1) | +2.50 (14/1/5) |
| exclude_mixed | −0.55 (5/3/12) | −0.05 (7/3/10) | +1.15 (13/3/4) | +1.15 (11/3/6) |
| unlabel_mixed | −0.40 (5/3/12) | +0.20 (11/0/9) | +1.25 (14/0/6) | +1.90 (13/1/6) |

In composition holdout the pair model reaches fewer positive systems than popularity at K=20 and K=50 in all policies, with 16–20 of 20 splits negative. At K=100 the differences are +0.95 (11/6/3), −2.60 (1/4/15) and −1.40 (4/5/11). At K=200 they are −0.15, −0.60 and −0.20.

**3. Cutoff ties make the small hit margins sensitive to tie order.** At K=100 a score tie crosses the cutoff in 16–20 of 20 splits for popularity and the pair model in every branch, but in only 3–8 splits for similarity. Holding saved scores fixed and reordering only within the crossing tie block gives the following range for pair − popularity system-holdout Hits@100 (`tie-sensitivity.tsv`):

| Policy | Least favourable tie order | Expected under random tie order | Most favourable | Saved order |
| --- | ---: | ---: | ---: | ---: |
| original | +3.50 | +8.01 | +12.90 | +7.95 |
| exclude_mixed | −2.00 | +1.21 | +4.20 | +1.35 |
| unlabel_mixed | −1.20 | +2.19 | +6.05 | +2.15 |

The saved hash tie order sits within 0.4 hits of the random-tie expectation for every score method. That gives no indication that the protocol's tie key favours any method. Only the original-policy hit advantage survives the least favourable tie order. The same caution applies to C4: the original-policy composition-holdout similarity − popularity margin of +0.50 spans −0.90 to +1.65 under tie reordering. The tie ranges describe composition hits; system metrics were not recomputed under alternative tie orders.

## Consequences for the claim ledger (file 02)

- **C5, refined:** "In system holdout at K=100, the pair model recovers more observed positives than popularity (+7.95, +1.35 and +2.15), and slightly more distinct positive systems (+2.80, +1.15 and +1.25). Both system-level scorers reach far fewer positive systems than uniform random selection or similarity at the same budget. The alternative-policy margins are within the range produced by cutoff-tie order alone and change sign at smaller budgets."
- **C7, completed for all methods:** concentration is shared with popularity and is not specific to the pair model. In system holdout at K=100, effective hit systems are 4.49/7.00/6.07 for popularity and 5.68/7.34/6.58 for the pair model, against 17.73/16.99/15.84 for similarity and 37.65/32.01/29.63 for random.
- **New candidate C15 (post hoc, measured):** composition Hits@K credits a method for filling its budget with many compositions from a few systems. In system holdout, the two rankers that lead on composition hits, the pair model and popularity, reach the fewest positive systems. In composition holdout, similarity leads on both measures, so the divergence depends on the design. This directly supports RQ2 and the unit-of-recommendation theme of framing A. It is a finding about the metric and the task, not about which ranking is scientifically preferable, and it does not treat element-set coverage as chemical diversity.

**Suggested Results sentence (provisional):**

> "On identical system-holdout pools, the pair model's Hits@100 margin over popularity was accompanied by 1.15–2.80 additional positive chemical systems on average. However, both system-level scorers reached 6–11 positive systems, compared with 20–24 for maximum similarity and 30–39 expected under uniform random selection. Composition-level recovery and system coverage therefore order the methods differently."

## Not established

- No significance testing, and no population inference. The splits overlap.
- Element-set coverage is not chemical, structural or functional diversity, and more systems is not automatically better for a user.
- Popularity and the pair model cannot separate stoichiometries within a system, so their low system counts are partly built into how they score, not an empirical defect. A system-level endpoint that ranks systems rather than compositions would be a different, new analysis. It is recorded in the parking lot and has not been run.

## Artifacts and reproduction

Row-level outputs are under ignored `reports/local/matched-system-metrics-2026-09-22/`:

- `system-metrics-by-split.tsv` (1,920 rows)
- `system-metrics-summary.tsv` (96 rows)
- `paired-differences.tsv` (288 rows)
- `tie-sensitivity.tsv` (48 rows)
- `primary-contrast.json`
- the Julia TSV copy
- `validation.json`, `report.md` and `SHA256SUMS.json`

Commands, run from the repository root; choose new output paths to repeat:

```sh
julia --startup-file=no --project=. scripts/matched_system_metrics.jl \
  reports/local/mp-system-holdout-v2-2026-08-31/results \
  reports/local/element-pair-evaluation-2026-08-31/results \
  reports/local/matched-system-metrics-2026-09-22-julia.tsv

python3 scripts/analyze_matched_system_metrics.py \
  reports/local/mp-system-holdout-v2-2026-08-31/results \
  reports/local/element-pair-evaluation-2026-08-31/results \
  reports/local/matched-system-metrics-2026-09-22 \
  --julia reports/local/matched-system-metrics-2026-09-22-julia.tsv \
  --prior-concentration reports/local/element-pair-diagnostics-stability-2026-09-07/analysis
```

The Julia script loads only `src/compositions.jl` and `src/ranking_evaluation.jl`, plus the one-line `chemical_system` definition, which it checks against `src/benchmark.jl`. This is because the full package did not load at the time: the uncommitted `src/evaluation_suite.jl` had a parse error at line 88 while another edit was in progress.
