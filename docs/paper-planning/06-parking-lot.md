# Parking lot

Preserve useful alternatives here instead of quietly deleting them during drafting. This investigation has not deleted or rewritten prior project documents. Entries below are material intentionally excluded from the main proposed argument, not a record that somebody else's manuscript was edited.

## Alternative framings and titles

| Material | Why outside the main narrative | Re-entry condition |
| --- | --- | --- |
| Full Eka research-software article covering SQLite adapters, imports, canonical types, CLI and audits | Broad engineering story dilutes the empirical result | Choose framing B; document distinct user need, comparable tools and independent usage/reproduction |
| New element-pair recommender method | Model family is established; gains conditional; factorization mechanism not isolated | Direct pair control, missing-weight ablation, fair system-level evidence and a meaningful literature contrast under new protocol |
| “Discovering unknown inorganic compounds with Eka” | Current task ranks already catalogued MP compositions with hidden provenance labels | New candidate universe, defensible independent outcomes and prospective experiment |
| “Chemical-system leakage explains inflated discovery performance” | Existing system and formula tasks change pools and prevalence; “leakage” and causality overreach | Matched controlled experiment and explicit definition of forbidden information |
| “A converged factor model for synthesis prediction” | Primary study deliberately fixed compute; later stationarity is post hoc; no synthesis endpoint | New prospective objective/evaluation and independent chemical outcomes |
| System-level endpoint: rank element systems (not compositions) and score positive systems in the top k systems | E1 shows composition Hits@K and system coverage diverge. Popularity and pair scores are constant within a system, so a system-level task may be their natural unit. Not run; it would be a new post-hoc analysis. | Co-authors want RQ2 answered at the system level; write a new E0-style specification before computing |
| Software-centered alternative title from file 03 | Useful if empirical distinction is too incremental | Co-author framing decision C1 |

## Prose and interpretations to retain only as notes

- The original narrative arc, “from reliable SQLite queries to experimental evaluation,” is useful background for a talk or development report. In the paper, one sentence in Methods suffices; Git chronology is not a Results section.
- `PROJECT_BRIEF.md` and `tmp/pdfs/build_dossier.py` contain a broad explanatory narrative, glossary, architecture illustration and older grouped-bar presentation. Retain them as resources. Do not reuse their causal wording, cross-design bar comparisons or unverified reference dates without checking the new audit.
- `docs/recovery-findings.md` says the similarity reversal identifies shared-system proximity as its mechanism. Preserve the idea as a hypothesis, and use the noncausal replacement in file 02.
- The original-policy pair mean of 52.25 Hits@100 is a useful anchor but a poor standalone headline: random expectation is 42.65 and hit concentration is substantial.
- The 17/24/22 system-disjoint hits are informative negative observations for the specified comparator/task. They are not evidence that system transfer is impossible or that materials outside familiar systems are unsynthesizable.
- “More reproducible” needs a comparator or a precise operational definition. Prefer reporting captured files, configuration identities, preserved environments and the actual checks performed.
- “All 120 fits converged” should be qualified as reaching the declared projected-gradient criterion in the later cap-sensitivity run, not proof of a global optimum.
- A ranker's direct access to held-out labels is a correctness concern; selection bias in which compounds enter MP is a scientific confounder. Avoid collapsing both into the word leakage.
- The independent Python metric fixture mirrors numerical expectations on a small hand-worked case. It does not by itself demonstrate cross-language equivalence on all real rankings.

## Useful engineering detail for supplement or software paper

Retain strict parsing, isotope exclusions, score-threshold conventions, SQLite schema adaptation, no-clobber import publication, Seko fixture attribution, warm versus first-query timing, public API classification, and cross-platform CI. They support software use and trust but do not each deserve a scientific contribution bullet.

The historical pair fit/rank phase times (18.71 s and 0.83 s) may be a short implementation note. Exclude broad speed or scalability claims without fresh workload/environment measurements. The old 4.7-million-row database validation concerns query tooling, not the MP recovery dataset.

## Experiments deliberately deferred

| Idea | Value | Why not needed now |
| --- | --- | --- |
| Direct raw pair frequency | Separates memorized pairs from completion; all-zero system-holdout control is mathematically informative | Needs new suite integration; does not decide whether observed evaluation sensitivity exists |
| Missing-pair alpha=0 ablation | Tests dependence on weak-zero assumption | Current implementation rejects alpha=0; new scientific code/protocol needed |
| Rank/initialization sweep | Numerical/model stability characterization | Must retain every run and prevent winner selection; cap sensitivity already supports narrower RQ3 |
| Richer stoichiometric or neural representation | Might resolve within-system ties | Changes model question substantially; not a fix for validity of current evidence |
| Chemical-family or leave-element-out holdout | Tests another transfer regime | Needs justified taxonomy/support and explicit cold-start interpretation |
| Matched prevalence/pool design | Could isolate parts of holdout effect | Separate estimand/protocol; descriptive paper can acknowledge confounding |
| Literature label adjudication | Can validate or recalibrate the proxy | Requires domain expertise and accessible primary synthesis reports; no outcome invented |
| Chronological split | Would move closer to forecasting | MP database timestamps are not first-discovery dates |
| Prospective synthesis or DFT | Independent chemical validation | Costly, outside this request, and a different endpoint |

## Cut-material log template

For each future cut, append: date; paragraph/figure ID; exact removed text or relative file pointer; reason (scope, evidence, repetition, style); useful future destination; evidence needed to restore it. Never overwrite the original source or rewrite frozen protocol text to fit a new narrative.
