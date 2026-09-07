# Recovery findings: completed benchmark series

The completed series compares three simple references and one fixed-compute
learned comparator on the same MP snapshot. All planned label policies and
holdout designs are retained; model settings were frozen before its real fits.

## All methods at top 100

Mean held-out experimental-provenance positives recovered across 20 splits.
Random expectation uses each split's actual candidate prevalence. Within each
row, all methods use exactly the same candidates and evaluation labels.

| Holdout | Label policy | Random observed | Random expected | Popularity | Similarity | Element-pair model |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| composition | original | 11.55 | 13.03 | 12.90 | 13.40 | 12.70 |
| composition | exclude_mixed | 9.05 | 10.10 | 14.70 | 17.75 | 12.75 |
| composition | unlabel_mixed | 7.85 | 8.64 | 11.30 | 14.10 | 10.15 |
| system | original | 43.35 | 42.65 | 44.30 | 29.85 | 52.25 |
| system | exclude_mixed | 35.95 | 35.81 | 46.45 | 26.75 | 47.80 |
| system | unlabel_mixed | 32.70 | 32.00 | 40.15 | 24.95 | 42.30 |

The similarity baseline is also a leakage diagnostic. It is the strongest method
under composition holdout, where candidates may share a chemical system with
training, but the weakest method under system holdout: its 29.85, 26.75 and 24.95
mean hits are all below the corresponding random expectations of 42.65, 35.81
and 32.00. Maximum cosine similarity to training is therefore useful chiefly when
system proximity is permitted; forbidding that proximity makes it
anti-predictive in these system-holdout pools.

Raw hit counts are not comparable between the two designs. Composition-holdout
pools are 8.64–13.03% positive, whereas system-holdout pools are 32.00–42.65%
positive. The favorable system-holdout hit totals therefore come from a much
denser evaluation task and exceed random expectation by 22–33%, not by the raw
difference between the designs' hit counts.

Under composition holdout the element-pair model trails popularity by 0.20,
1.95 and 1.15 mean hits across the three policies, and trails similarity by
0.70, 5.00 and 3.95. Under system holdout it leads popularity by 7.95, 1.35
and 2.15, and similarity by 22.40, 21.05 and 17.35. The smaller margins under
the alternative label policies constrain any general claim about its benefit.

The original-label system advantage over popularity is positive in 13 splits,
zero in two and negative in five. Excluding mixed labels gives 12 positive,
two zero and six negative splits; unlabelling mixed groups gives 12 positive,
one zero and seven negative splits. These overlapping splits describe sensitivity,
not independent replications or statistical significance.

The composition-holdout subgroup diagnostic is negative for transfer to unseen
systems. Only 16–22% of held-out positives are system-disjoint. Across all 20
overlapping splits, the fixed-compute model recovers 17, 24 and 22 such positives
at top 100 under the original, exclude-mixed and unlabel-mixed policies, versus
uniform-random expectations of 42.13, 45.04 and 38.53. These small event counts do
not support precise ratio estimates or confidence intervals. They show no
demonstrated ability to prioritize system-novel positives; the composition-holdout
signal is concentrated among positives whose chemical system occurs in training.

The system-holdout top 100 also has a smaller effective decision count than its
100 rows imply because all stoichiometries in a system share a score. Under the
original policy it contains a mean 13.5 distinct systems, only 9.0 systems supply
any positive hit, and concentration of hits corresponds to 5.68 equally weighted
systems by inverse Herfindahl index. The largest system supplies 27.9% of hits on
average, and one system can occupy 52 of 100 rows. Exclude-mixed and unlabel-mixed
top-100 lists average 14.55 and 13.20 systems and 7.34 and 6.58 effective hit
systems. The 52.25 mean therefore describes clustered composition hits from a
small number of system-level ranking decisions.

## What the series establishes

The original similarity comparator has a small composition-holdout advantage
under the original label rule. Its magnitude depends on mixed-flag treatment,
and its reversal to below-random performance under system holdout identifies
shared-system proximity as the mechanism behind that advantage. The pair-factor
model improves mean system-holdout results on denser pools, but those hits are
clustered in a small number of system decisions. It does not improve the sparse
composition comparison and shows no demonstrated recovery ability within that
design's system-disjoint subgroup.

This task recovers withheld provenance labels from a single contemporaneous MP
snapshot: it is partition reconstruction, not chronological discovery prediction.
This is evidence about the specified recovery tasks and fixed configurations,
not synthesis success, a universal ranking method, or a causal effect of chemical
separation. System pools have different sizes/prevalence and can still contain
close chemical analogues to training. Unlabelled does not mean failed synthesis.
The MP experimental-provenance flag is a proxy; none of the alternative policies
has been independently established as ground truth.

## Model and numerical limitations

The model uses only non-O element-pair counts. All stoichiometries in a system
tie; the predefined hash resolves their order. Missing pairs are weak zero-target
associations, not verified-negative compounds. Cold elements receive explicit
zero scores and are never silently dropped. Factors can reflect research frequency.

**101 of 120 real fits hit the 2,000-iteration cap; 19 met the declared stationarity
criterion.** This was anticipated in synthetic feasibility and frozen as a
fixed-compute evaluation. The results do not establish converged or global optima.
No hyperparameter, initialization, iteration checkpoint or favorable policy was
selected after inspecting the learned results. These are not Seko model predictions.

A post-hoc stability run changed only the cap from 2,000 to 20,000 iterations.
All 120 fits then met the same stationarity criterion by iteration 11,309. None of
the 19 already-converged top-100 lists changed, but 55 of the 101 previously capped
lists changed, with as many as 48 of 100 compositions replaced. Top-100 hit deltas
averaged +0.16 and ranged from -5 to +4, so aggregate means were comparatively
stable while individual recommendations were compute-budget-sensitive. The
converged sensitivity recovered 18, 26 and 23 system-disjoint composition-holdout
positives across the three policies; this does not change the negative subgroup
interpretation above. The prospectively frozen 2,000-iteration result remains the
primary result; the later run characterizes its stability rather than replacing it.
The exact runner, independent analyzer, synthetic corruption tests and local
hashed-evidence boundary are documented in [the element-pair execution record](mp-element-pair.md#post-hoc-diagnostics-and-stability).

## Reproduction and artifact boundaries

The original pilot, both sensitivity modes and system-holdout evidence remain
unchanged. Composition reference controls match the saved full-pipeline sensitivity.
The learned runner pins v2's config, verifies its inventory and source, and
reconstructs all memberships before fitting. Alternative policies with identical
training sets reproduce identical factor matrices and optimizer traces.

Local validation passed 4,583 Julia checks and 36 Python tests after the
[audit hardening compatibility check](audit-hardening-compatibility.md). The independent
learned analyzer reconstructs membership, pair counts, metrics and coverage,
recomputes every score and the final objective/gradient from factors, and rejects
rehashed corruption. Complete refitting reproduction and inventories are recorded
with the local evidence; do not substitute saved-score checks for that refit.

See [pilot reproduction](mp-pilot-reproduction.md),
[label sensitivity](mp-label-sensitivity.md),
[system holdout](mp-system-holdout.md), and
[element-pair execution/evidence](mp-element-pair.md).
Those guides identify the frozen protocols and local restore instructions.
The tracked package includes source, synthetic workflows, methods and this
attributed aggregate summary. Record-level data, factors, rankings and environments
remain local; public exact real reproduction requires separately available input
artifacts. No data bundle, new API query or provider message was sent.

## Attribution and handling

Data source: [Materials Project](https://materialsproject.org/), database version
2026.04.13, API snapshot retrieved 31 August 2026 at 12:16:39 UTC. Eka normalized
and grouped compositions, applied the declared label policies, constructed the
holdouts and computed scores and metrics; GNoME was excluded. These analyses do
not imply provider endorsement. The [supplied terms review](mp-terms-evidence.md)
records the CC BY 4.0 basis for covered content and its provenance limits.
Original Eka code is MIT; third-party notices remain separate.

Reference: A. Jain et al., “Commentary: The Materials Project: A materials genome
approach to accelerating materials innovation,” APL Materials 1, 011002 (2013),
[doi:10.1063/1.4812323](https://doi.org/10.1063/1.4812323).
The learned-method references and exact assumptions are in its
[specification](mp-learned-feasibility.md).

## Reassessment

The planned benchmark series is complete locally. Do not start a larger or tuned
model merely to improve the table. The useful next commitment is review of these
findings and the permitted sharing package. Any convergence study, stoichiometric
extension, tuned model or literature-label audit should begin with a separate
question and prospective protocol. Full Seko reproduction and production deployment
remain outside this work.

Any future rank or initialization study must be prospectively framed as stability
characterization, predeclare its ranks, restarts and consensus metrics, report every
run, and retain the frozen rank-4 fixed-compute result regardless of the sweep.

The separate-checkout refit reproduced all 992 deterministic files,
the complete configuration and all six analysis files exactly. Julia tests also
passed in that checkout. The captured Manifest was unchanged. This is same-platform
reproduction using an existing depot, not an empty-depot or cross-platform claim.

Measured across the real run, fitting totaled 18.71 seconds and ranking 0.83
seconds (excluding input verification, file output, analysis, process startup and
reproduction). These are measured computation costs, not a recorded total of
implementation effort or a commitment to a larger model-development schedule.
