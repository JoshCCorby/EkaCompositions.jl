# Repository and research-history map

## Scope and state

Inspected the repository, ancestor instruction locations, tracked and ignored research artifacts, local branches/tags and locally available remote-tracking refs on 22 September 2026. No applicable `AGENTS.md` was found. `CONTRIBUTING.md` requires preservation of frozen protocols and hashed source paths; it also keeps real records and detailed derivatives under ignored `data/local/` and `reports/local/`. This package follows those conventions, including relative paths in tracked documentation.

HEAD is `0629ba9` (`v0.1.1`, local main and origin/main). The initial working tree already modified `CHANGELOG.md`, `docs/api-stability.md`, `docs/make.jl`, `docs/src/api.md`, `src/EkaCompositions.jl`, `test/runtests.jl` and `test/test_api.jl`; it also contained untracked `PROJECT_BRIEF.md`, the evaluation roadmap/metric contract, two source modules and three tests. None is part of the tagged release merely because it loads in this checkout. See the verification record for the exact separation.

Existing research prose includes the frozen protocols, execution reports, `docs/recovery-findings.md`, the untracked `PROJECT_BRIEF.md`, and the local dossier `output/pdf/eka-recovery-project-research-dossier.pdf` with generator `tmp/pdfs/build_dossier.py`. The generator and brief were inspected as earlier narrative work; the PDF was identified, not visually audited. No current manuscript `.tex`, bibliography `.bib`, or notebook `.ipynb` was found in the repository search. Saved PNG/SVG pilot figures live inside local evidence bundles; they are not automatically submission-ready.

## Problem, users and actual workflow

The initial documented purpose was reliable exploration of precomputed composition scores in SQLite, for researchers working with inorganic composition recommendation. `git show 7fea48d:README.md` explicitly calls it scientific software engineering rather than a new prediction model. The later research workflow asks how simple training-only rankings recover withheld database provenance positives. The broader appeal is to materials-informatics researchers evaluating what a composition recommender actually learns.

Two workflows must be kept distinct:

- **Stored-score tool:** SQLite or scored TSV → strict canonical compositions → schema-aware filters/import validation → stored-score or reference-cosine ordering → CLI/library rows. It does not generate the upstream scores.
- **Research experiment:** preserved MP JSONL/TSV and query metadata → audit and composition grouping → policy-dependent labels → composition or system splits → training-only rankers → evaluator attaches held-out labels → fixed-budget metrics, full rankings and provenance → independent Python analysis. The pair model is trained here, separately from the SQLite path.

## Implementation map

Line references describe the inspected working tree; historical results bind their own captured bytes, not these mutable line positions.

| Component and evidence location | Actual behavior | Scientific role/status |
| --- | --- | --- |
| `bin/eka`; `src/EkaCompositions.jl:16–53`; `src/cli.jl` | Library exports, CLI dispatch and internal `Research` modules | Implemented entry points; packaging is supporting infrastructure. |
| `src/compositions.jl`; `test/test_compositions.jl` | Strict element/integer parser, repeated-element summation, ratio reduction, canonical ordering, equality/hashing | Central to the unit of evaluation and preventing equivalent-formula overlap. No structures, isotopes, charges or fractional occupancies. |
| `src/database.jl:26,43,147,187`; `src/import.jl:15,111` | Read-only SQLite adapter; full audit; transactional no-clobber scored imports | Implemented/tested infrastructure. Source scores retain their upstream meaning. |
| `src/ranking.jl`; `src/benchmark.jl:27,141` | Stored-score/cosine strategies and a separate binary-label benchmark | Implemented/tested; binary examples are synthetic correctness evidence. |
| `scripts/export_mp_pilot.py`; `scripts/requirements-mp.txt` | Optional pinned Python MP client exporter, explicit selected fields/query metadata | Real retained snapshot exists; network exporter is unnecessary for offline reproduction. |
| `src/mp_audit.jl:111,184–245` | JSONL/TSV verification; valid-scope records grouped by canonical composition; false flag takes positive precedence | Implemented, tested, used on real input. Provenance proxy, not validated synthesis. |
| `src/mp_recovery.jl:63,131,213` | Deterministic formula holdouts; pinned source/protocol checks; separate ranker inputs and evaluator files | Central implemented methodology. |
| `src/mp_pu.jl:125–210,222–236` | Streaming max cosine, popularity and hash-random rankings; Hits, recall, enrichment and exact random expectations | Central implemented/tested/measured references. |
| `src/mp_label_sensitivity.jl:14–48,101` | Original, exclude-mixed and unlabel-mixed policies; fixed-ranking relabelling versus full-pipeline rebuild | Central completed label sensitivity; those two modes answer different questions. |
| `src/mp_system_holdout.jl:18–50,62,147` | Common system universe; hash-selected fifth of systems; all candidates restricted to selected systems | Central completed evaluation-design comparison. |
| `src/element_pair_model.jl:11–17,34–72,87–136`; `src/mp_element_pair.jl` | Rank-four weighted symmetric nonnegative factorization of non-O pair counts; deterministic optimization, cold-element zero fallback, system-level ties | Implemented/tested/measured comparator; no stoichiometry resolution within a system. |
| `scripts/analyze_element_pair.py:24,42,136`; other `analyze_*.py` | Independent reconstruction of memberships, metrics, factor scores and numerical state; inventory and corruption checks | Strong correctness/reproducibility evidence, not independent replication on new data. |
| `scripts/run_element_pair_stability.jl`; `scripts/analyze_element_pair_stability.py:26–147` | Post-hoc cap increase to 20,000 and subgroup/concentration diagnostics | Released in v0.1.1; real local evidence exists. |
| `src/ranking_evaluation.jl:63–136`; `src/pair_frequency_model.jl:30–71` | Reusable system-aware metrics and raw pair-frequency control | Uncommitted implementation; 75 focused Julia checks passed in this investigation. No frozen new real suite/result found. |
| `docs/evaluation-roadmap.md` | New result schema, missing-pair ablation, suite v3, scaling and possible richer models | Plans only where no corresponding runner/protocol/results exist. In particular alpha=0 is rejected by current factor settings validation (`element_pair_model.jl:22`). |

Dependencies are small: Julia ≥1.10, SQLite/DBInterface, ArgParse, JSON3, SHA/TOML/Dates/Printf and PrecompileTools (`Project.toml`). `Manifest.toml` exists locally; historical experiments preserve their own exact environment. Python analyzers use the standard library; MP acquisition has separate optional dependencies. Documenter and CI are supporting infrastructure. Tests include hand-computed metrics, formula identity, disjointness, deterministic ranking, factor gradients, cold coverage, label isolation and tampering with rewritten checksums. They cannot validate a provenance label's chemical truth.

## Research trajectory: meaningful changes

Dates and motivations below come from inspected commits, protocols and execution records. Interpretation is explicitly marked. Git commit dates alone do not establish that an experiment was prospectively frozen.

| Date / commit | Change material to the paper | Motivation/evidence and interpretation |
| --- | --- | --- |
| 30 Aug, `7fea48d` | Reusable score-query package with scientific limitations already stated | Original README documents software-engineering motivation. No evidence for an original novel-model goal. |
| 31 Aug, `a8d8231`, `221c53b` | Binary fixed-budget benchmark; MP exporter and provenance audit | Shift from querying supplied scores to constructing inspectable evaluations. Synthetic benchmark is not a research result. |
| 31 Aug, `aed4883`, `4b07e95`, `1a01a41`, `9d1b836` | Frozen PU recovery protocol, verified formula splits, evaluator, training-only maximum cosine | Protocol defines the question, source identity and seeds. Inspecting code confirms separation of ranker formulas from evaluation labels. |
| 31 Aug, `568ed60` | External Seko scores excluded before recovery scoring | New provenance review reports missing training membership/cutoff and label-dependent coverage. This avoids an ineligible comparison, not a failed model result. Clean commit used for the original pilot. |
| 31 Aug, `67f8ad0` | Independent pilot analysis and mixed-label sensitivity | Protocol says follow-on after original pilot. Interpretation: investigates dependence on provenance aggregation; does not establish a correct ground-truth policy. |
| 31 Aug, `260d14c` | Chemical-system holdout and reproduction package | Follow-on protocol addresses same-system proximity. Code changes the candidate pool as well as the separation rule, so design effects are confounded. |
| 31 Aug, `415f363` | Fixed-compute element-pair comparator and combined findings | Synthetic feasibility and frozen settings support one additional comparator. Captured source overlay is needed to identify execution code exactly. |
| 31 Aug, `b1d3ef5`, `32edc74` | Audit hardening and compatibility documentation | Diffs add JSONL/TSV consistency checks and allow a pinned historical audit-code hash while reconstructing scientific fields. Evidence-integrity fix, not a new result. |
| 4 Sep, `f4546c4`, `03704c3` (v0.1.0), `ae3684f` | Offline tools moved to Julia; package renamed; research modules isolated | Important reproduction drift from old `Eka.jl` snapshots. Scientific implementation identity must follow captured files, not current package name. |
| 7 Sep, `585b621`, `0629ba9` (v0.1.1) | Limitations sharpened; executable subgroup/concentration and 20k stability analysis added | Diff corrects the narrative toward prevalence, clustered hits and recommendation instability. Post-hoc evidence must remain labelled post hoc. |
| Working tree, not dated by Git | General metrics and pair-frequency modules, tests, roadmap and project brief | Useful next-stage work. No scientific claim should credit these with producing the August results. |

## Historical run identity versus current source

| Evidence bundle under `reports/local/` | Execution identity actually recorded | Traceability and limitation |
| --- | --- | --- |
| `mp-recovery-pilot-v1-2026-08-31` | Clean `568ed605c131edfa40695afc53781015c9739f6c`; `freeze.json` | Commands, source archive, Manifest, results and clean-checkout comparisons retained. Original report says 240 metric rows. |
| `mp-label-sensitivity-v1-2026-08-31` | Base `568ed60` plus dirty/untracked overlay; `implementation-freeze.json` | Base commit alone is insufficient; `environment/source-tree.tar` and patch bind exact code. Saved reproduction: 925 deterministic files, 1,440 metric rows. |
| `mp-system-holdout-v2-2026-08-31` | Base `baec7e3` plus captured overlay; archive SHA `76eae73935459d70fa38c6f71fc1cbba60a7df7394e20e38d89c95402a028e0b` | `REPRODUCE.md`, argument-array command record, config and environment exist; 1,472 deterministic files checked now. |
| `element-pair-evaluation-2026-08-31` | Base `433dfbb` plus captured source archive SHA `b60a4863d68a76787f7be352f9986e73c5693e7e03a2b862751ae611825a7dc7` | 120 fits/480 new metric rows. Saved reproduction reports full refit equality; 992 deterministic files checked now. |
| `element-pair-diagnostics-stability-2026-09-07` | v0.1.1-era implementation hashes in stability config | Post-hoc evidence. Current wrapper includes uncommitted changes; a verifier requiring current source equality may fail without invalidating retained results. Restore recorded source or compare recorded identities explicitly. |

All principal real studies use the same 2026.04.13 MP snapshot, retrieved 31 August at 12:16:39 UTC. Frozen protocol language such as “not implemented” describes its freeze-time state, not today's implementation. Earlier “permissions unresolved” statements likewise need dated interpretation; the later permissions register is separate from immutable experiment records.

Available refs: main, origin/main, v0.1.0/v0.1.1 and five origin/dependabot refs. `git log --all --not main` finds only two unmerged CI update commits (`5830a2e`, `91c8382`); no alternative research branch was found. This is a local-ref inventory, not a fresh remote fetch. Earlier removed docs and offline Python tools remain accessible in history and the source archives. Commit counts do not establish scientific credit or author order.
