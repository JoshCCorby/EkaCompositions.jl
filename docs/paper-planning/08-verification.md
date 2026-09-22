# Investigation verification record

Date: 22 September 2026. HEAD: `0629ba9d600afcd0cdbf1ddfc30ef83dbe6088c4`. Environment observed: Julia 1.12.6; Python 3.14.6; Darwin arm64. New verification artifacts are isolated under ignored `reports/local/paper-planning-audit-2026-09-22/`. Existing evidence was read without overwriting it.

## Checks actually performed now

| Check | Result | What this does and does not establish |
| --- | --- | --- |
| System-holdout saved deterministic inventory | 1,472 file hashes matched `results/config.toml` | Internal identity/integrity; not independent authenticity of upstream records |
| Primary element-pair saved deterministic inventory | 992 file hashes matched `results/config.toml` | Includes captured evidence files; does not itself refit the model |
| Saved primary and 20k stability reanalysis | Existing `scripts/analyze_element_pair_stability.py` completed successfully | Its validator checks complete run inventories, captured source/implementation, membership, ranking, factor scores, metrics, final objective/gradient, diagnostics and source agreement. It does not rerun optimization. |
| Comparison with original stability analysis | All 11 files byte-identical, including `SHA256SUMS.json` | Independent execution of the existing analyzer, not a newly independently authored implementation or a new dataset |
| All-method summary arithmetic | Recomputed 96 method/design/policy/budget summary rows from 1,920 raw metric rows, 20 splits each; four mean fields agree within 10⁻¹² | Checks averaging of hits, recall, enrichment and random expectation; complements saved-ranking validation; not a fresh scientific run |
| Grouped-audit counts | Recounted 12,506 groups, 5,359 positive, 7,147 unlabelled, 1,343 mixed, 2,630 systems | Recount of retained grouped input; does not chemically adjudicate labels |
| Targeted new Julia metric tests | 23 main arithmetic + 29 edge/validation checks passed | Current dirty-tree module is implemented/tested, not evaluated on a new real suite |
| Targeted new Julia pair-frequency tests | 23 checks passed | Count/scoring/determinism and all-zero grouped-holdout behavior; no evidence of real ranking superiority |
| Python hand-worked metric oracle | 2 tests passed | Independent arithmetic on one fixture and no-hit case; not automatic full Julia/Python cross-language comparison |
| Current source versus stability implementation hashes | `src/EkaCompositions.jl` differs; other recorded paths match | Confirms current dirty wrapper is not the exact old execution tree; old result identity is carried by captured source |

## Input and run identifiers

| Artifact | SHA-256 |
| --- | --- |
| `data/local/mp-ternary-snapshot/snapshot.toml` | `5c82fb38f90105a03779daab0cb32f2ba134cb1ce50cf94e845b38e92719ad58` |
| Snapshot `records.tsv` | `98a6ce78d592e5e7e4cef98d675badcf991cc2caecef9a6b0ec10c1e08731a08` |
| Snapshot `records.jsonl` | `5ba17f307d61c9635a93f75fe86afc9e81af430036f3ef1fc0fe199a75f3829b` |
| Audit `audit.toml` | `c63f465ab9104508b5a08f4a3263d267842b06d94954d0479e3662da7268eefa` |
| Audit `compositions.tsv` | `722ecf2e40a99c59b0f024219782a1fe8791f000353cd5e6cf7faa1ef6e5213d` |
| v2 system `results/config.toml` | `c55cc2cf29f75b74abda3dc66194043339b564cf1614d925434adcb581932565` |
| Primary pair `results/config.toml` | `f7b4d6268ed29ed10e60d53c6d31a49673cf9b218af3c369f21e885cf8d94525` |
| Stability `stability-results/config.toml` | `4062c98bcc313ab79f87f00b841f860a0a1c6fc0056f1ee0a2e101acc65e69d3` |

Source identity is distinct from provenance truth and permission. No fresh MP request, source-term legal determination or upstream authenticity certification was attempted.

## Commands used for substantive checks

Run from repository root. The output path below is the one created during this investigation and now exists; for repetition choose a new sibling directory rather than overwriting it.

```sh
python3 scripts/analyze_element_pair_stability.py \
  reports/local/element-pair-evaluation-2026-08-31/results \
  reports/local/element-pair-diagnostics-stability-2026-09-07/stability-results \
  reports/local/paper-planning-audit-2026-09-22/stability-reanalysis

julia --startup-file=no --project=. -e \
  'using Test, Random, SHA, EkaCompositions; include("test/test_ranking_evaluation.jl"); include("test/test_pair_frequency_model.jl")'

python3 -m unittest discover -s test -p 'test_evaluation_metrics.py'
```

Additional short Python checks read `deterministic_file_hashes` from each config and compared SHA-256 of every named file, byte-compared each old/new analysis file, counted labels/systems from grouped TSV, and regrouped raw metrics by `(design,policy,budget,method)` to compare 20-split means. The resulting local records are `inventory-checks.json`, `analysis-comparison.json`, `source-identities.json`, `summary-arithmetic.json`, `current-source-drift.json`, `environment.txt`, and the two targeted-test logs. `audited-working-tree.patch` captures the pre-existing tracked changes, not a proposed application patch.

## Reported in historical artifacts, not newly repeated

- Pilot: clean-checkout regenerated memberships, rankings and metrics, with the documented producer-manifest difference; `mp-recovery-pilot-v1-2026-08-31/reproduction-checks.json`.
- Label sensitivity: 925 deterministic files and 1,440 metric rows matched after restoring captured overlay.
- System holdout: 1,472 deterministic files and full config matched in historical rerun.
- Pair model: 992 deterministic files and all six primary analysis files matched after full refitting, according to the retained record.
- Historical large test counts in project documentation (for example 4,583 Julia checks) describe the then-current state. They are not test totals for this investigation.

A current-source verifier in the stability bundle requires today's implementation hashes to equal recorded ones. We inspected that verifier rather than misreporting a current-tree execution as successful: the changed wrapper would fail the equality check. The saved-run analyzer instead validates the captured implementation bytes and successfully reproduced the saved diagnostics. Neither fact justifies silently ignoring code drift in a full refit.

No application code was changed; no full application suite, production database benchmark, model training, convergence rerun, dependency update, clean-environment installation or cross-platform reproduction was performed. The verification scope is sufficient to audit the planning claims but should not be expanded into a stronger reproducibility statement.

## Addendum: E1 matched system metrics (22 September 2026)

Performed after the investigation above, under the [E0 specification](09-e0-system-metrics-spec.md). Outputs are under ignored `reports/local/matched-system-metrics-2026-09-22/`. Commands are in [file 10](10-e1-system-metrics-results.md).

| Check | Result | What this does and does not establish |
| --- | --- | --- |
| Input inventory | 842 files hash-matched their bundle `config.toml`; pair and v2 memberships hash-equal for all 120 branch/splits | Every method's ranking was scored against the same held-out set; not upstream authenticity |
| Saved metric agreement | 1,920 of 1,920 recomputed (Hits@K, N, \|R\|) rows equal the saved `metrics.tsv` | The system metrics join the same rankings that produced the published hit counts |
| Julia versus Python | All shared integer, float and tie fields agree; maximum float difference 0.0 | Two implementations agree; both depend on the same saved rankings |
| Prior pair concentration | All 60 v0.1.1 `system-concentration-by-split.tsv` rows reproduced | Consistent with the earlier analyzer |
| Hand-worked rows | Two rows recomputed from `awk` counts; exact agreement | Arithmetic spot check only |
| Determinism | Two runs with different `PYTHONHASHSEED` values produced identical `SHA256SUMS.json`. An earlier run varied in the last bits of `random_expected_hit_systems`; fixing the float summation order resolved it before the retained output was generated | The analyzer's own output is repeatable; not a fresh experiment |

The Julia check loaded only the metric kernel files, because the full package failed to load. The uncommitted `src/evaluation_suite.jl` had a parse error at line 88 while it was being edited. Kernel file hashes are recorded in `validation.json`. No model fitting, MP query or application-code change was involved.
