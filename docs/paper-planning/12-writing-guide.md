# Writing guide: typing up the paper

Keep this open beside the manuscript. For each part of the paper it tells you what to write, which files to open (paths from the repository root, with line numbers), which numbers to use and where to verify them, and what not to claim.

Prepared 22 September 2026. Short names such as `03-manuscript-skeleton.md` are files in `docs/paper-planning/`; all other paths start at the repository root. Line numbers refer to the files as committed on that date. If you edit a planning file, its headings are still the reliable anchors.

- **Order to write in:** Methods → Results → Introduction → Discussion → Abstract. The guide below is in reading order.
- **Length:** 3,500–4,500 words of main text (`docs/paper-planning/03-manuscript-skeleton.md:5`). Rough split: Introduction 700, Methods 1,200, Results 1,200, Discussion 800, Abstract 200.
- **Figures and tables:** all are in `reports/local/paper-figures-2026-09-22/`, as vector PDF for the manuscript and PNG for previews. Draft captions are in `captions.md` in the same folder.

To regenerate them, choose a new output folder and run:

```sh
.venv-mp/bin/python scripts/make_paper_figures.py reports/local/paper-figures-NEW
```

## Step 0 — before typing

1. **Confirm the framing.** Framing A is a bounded empirical evaluation study (`docs/paper-planning/02-evidence-and-framing.md:64-70`); the literature pass supports it (`docs/paper-planning/11-l1-nearest-work.md:53-55`). Record your decision in the decisions table (`docs/paper-planning/05-backlog-and-decisions.md:47`).
2. **Choose the title** (`03-manuscript-skeleton.md:7-13`). Since E1, alternative 1, *From composition hits to chemical systems…*, fits the strongest finding best.
3. **Update the thesis sentence** (`03-manuscript-skeleton.md:15`) to name the counted unit, for example: *"…label policy, holdout design and the unit counted change the apparent benefit of composition-ranking methods…"*.
4. **Keep the three research questions** (`03-manuscript-skeleton.md:17`). RQ2 now has a complete answer.
5. **Create the manuscript file.** LaTeX suits a journal or arXiv, and the figures are already PDF.

## Rules that apply everywhere

Keep these beside you and check every paragraph against them.

| Rule | Why / source |
| --- | --- |
| Call the endpoint **"withheld Materials Project experimental-provenance labels"**. Never "synthesizability", "discovery" or "synthesis success". | `02-evidence-and-framing.md:25` (C13), `:33` |
| Every number carries its **design, policy and K**. "Similarity is best" is never a sentence. | `02-evidence-and-framing.md:60-62` |
| Splits are **20 overlapping holdouts**: descriptive, with no p-values, confidence intervals or "significant". | `02-evidence-and-framing.md:41` |
| Hits/K is **not precision**. Mean enrichment is the **mean of per-split ratios**. | `02-evidence-and-framing.md:39` |
| Never compare raw hits **across designs**: the candidate pools differ (see Table 1). | `03-manuscript-skeleton.md:133` |
| Label **post hoc** material as such: subgroup, concentration, 20k stability, E1 system metrics and tie ranges. | `09-e0-system-metrics-spec.md:3`; `03-manuscript-skeleton.md:117-119` |
| No **"first"** or "novel metric". The system-unit finding applies virtual-screening and recommender-systems ideas. | `11-l1-nearest-work.md:47` |
| Use the **similarity reversal sentence** from the planning file verbatim or close to it; do not say the reversal "identifies the mechanism". | `02-evidence-and-framing.md:62` |
| Copy numbers from the **TSV/MD tables**, not from prose. Recheck each one before sharing the draft. | Folder list in *Final checks* |
| Cite only **verified references** (L1–L15). Items marked \* in file 11 need a human read before you cite their specifics. | `07-literature.md:7-26`; `11-l1-nearest-work.md:25` |

---

## Introduction (about 700 words, 4 paragraphs)

The skeleton for all four paragraphs is at `03-manuscript-skeleton.md:27-61`.

### I1 — Why rank compositions, and what a label means

- **Write:**
  - Large inorganic composition spaces motivate prioritization, and database-informed recommenders are one route to it.
  - Databases mix experimental and computational records, so evaluation depends on what the label represents.
  - End on your topic sentence (`03-manuscript-skeleton.md:37`).
- **Open:**
  - Sentence plan at `03-manuscript-skeleton.md:29-37`.
  - Seko 2018 and Jain 2013 at `07-literature.md:11-12`.
  - Hayashi 2022 review at `07-literature.md:25`.
  - How Seko and Hayashi evaluate at `11-l1-nearest-work.md:19-20`: top-N discovery rate against other databases.
- **Cite:** L1, L2, L14.
- **Don't:** quote a size for chemical space or laboratory costs without a source (`03-manuscript-skeleton.md:35`).

### I2 — Prior approaches and what they measure

- **Write:**
  - Positive-unlabelled (PU) synthesizability models differ in inputs and endpoints: Chung (composition, curated solid-state labels); SynthNN (ICSD versus generated formulas); SynCoTrain (structure, MP experimental/theoretical flag).
  - Prior work already discusses chemical-system familiarity and label-scheme dependence: Chung §3.5.4 and models 1 vs 2.
  - Nominal out-of-distribution splits can remain interpolation (Li); clustered data inflates performance (Meredig).
- **Open:**
  - Comparison table at `11-l1-nearest-work.md:13-23`.
  - "Shared and not new" list at `11-l1-nearest-work.md:29`.
  - Reference rows at `07-literature.md:13-18,24`.
- **Numbers:**
  - Chung: 141 of 168 predictions (83.9%) fall in chemical systems with a known training positive; ROC AUC is 0.921 vs 0.771 between label schemes (`11-l1-nearest-work.md:16`).
- **Before citing SynCoTrain or Li specifics:** read them yourself; they are marked \* at `11-l1-nearest-work.md:25`. SynCoTrain matters most, because its endpoint is close to yours.
- **Don't:** compare anyone's headline accuracy with Eka's Hits@100 (`07-literature.md:30`).

### I3 — The specific gap

- **Write:**
  - A fixed row budget can credit many stoichiometries from one element set.
  - Virtual screening handles this with chemotype-aware counting (Clark & Webster-Clark; Mackey & Melville), and recommender systems treat coverage as a standard objective beyond accuracy.
  - In the materials composition-recovery studies examined, system coverage of held-out hits is not reported.
  - Label rules and holdout construction also change the populations, and stable averages can hide changed recommendations.
- **Open:**
  - Sentence plan at `03-manuscript-skeleton.md:47-53`.
  - C15 novelty check at `11-l1-nearest-work.md:38-47`.
  - References at `07-literature.md:20-23` (L9–L12).
- **Wording:**
  - Write "in the studies we examined", never "no study has".
  - The Chung familiarity statistic is the closest materials analogue. Say it measures familiarity, not coverage (`11-l1-nearest-work.md:45`).

### I4 — Questions and contribution

- **Write:**
  - The three research questions in one sentence.
  - The setting: one snapshot, two holdouts, three policies, four rankers, four budgets.
  - The contribution sentence (`11-l1-nearest-work.md:51`).
  - An explicit list of exclusions (`03-manuscript-skeleton.md:59`).
- **Open:** `03-manuscript-skeleton.md:55-61`.

---

## Methods (about 1,200 words)

Most paragraphs already have provisional prose in the skeleton. Your job is to check each sentence against the source listed and tighten it.

### M1 — Snapshot

- **Prose:** `03-manuscript-skeleton.md:69`.
- **Verify:** `data/local/mp-ternary-snapshot/snapshot.toml:1-19` (database version 2026.04.13, retrieved 2026-08-31T12:16:39Z, mp-api 0.46.5, `include_gnome=false`, three elements including O); 24,020 records in `records.tsv`; data identity in `docs/mp-recovery-protocol.md:27-51`.
- **Cite:** L2.

### M2 — Canonical compositions and label policies

- **Prose:** `03-manuscript-skeleton.md:75`.
- **Verify:**
  - Grouping in `src/mp_audit.jl:184-227`.
  - Policies in `src/mp_label_sensitivity.jl:14-38` and `docs/mp-label-sensitivity-protocol.md:36-46`.
  - Full-pipeline rebuild in `docs/mp-label-sensitivity-protocol.md:75-95`.
- **Numbers** (Table 1 footnote, `reports/local/paper-figures-2026-09-22/t1-populations.md`): 12,506 compositions; 5,359 positive and 7,147 unlabelled; 1,343 mixed; 2,630 systems.
- **Must say:** no independent chemical audit of the labels exists.

### M3 — Holdouts

- **Prose:** `03-manuscript-skeleton.md:81`.
- **Verify:**
  - Code: `src/mp_recovery.jl:63-99` and `src/mp_system_holdout.jl:18-50` (`universe`, `selections`, `system_splits`).
  - Protocols: `docs/mp-recovery-protocol.md:80-127` and `docs/mp-system-holdout-protocol.md:26-81`.
- **Numbers:** 526 of 2,630 systems selected (Table 1).
- **Optional:** the split diagram at `04-figure-storyboard.md:76-98`, only if the text alone is unclear.

### M4 — Reference rankers

- **Prose and equations:** `03-manuscript-skeleton.md:87-94`.
- **Verify:**
  - Popularity, cosine, random and tie rule in `src/mp_pu.jl:125-210`; `pu_rank` is at line 180.
  - Allowed inputs in `docs/mp-recovery-protocol.md:128-161`.
  - Seko score exclusion in `docs/mp-external-score-provenance.md:51-87`.
- **Don't:** imply the Seko exclusion says anything about Seko's accuracy (C14, `02-evidence-and-framing.md:27`).

### M5 — Element-pair comparator

- **Prose and objective:** `03-manuscript-skeleton.md:100-107`.
- **Verify:**
  - Settings and objective in `src/element_pair_model.jl:11-72`.
  - Fitting in `src/element_pair_model.jl:87-118`.
  - Scoring in `src/element_pair_model.jl:119-130`: the score is constant within a system.
  - Ranking in `src/element_pair_model.jl:131-136`.
  - Protocol in `docs/mp-element-pair-protocol.md:9-55`.
- **Cite:** L6, L7.
- **Stress:** every stoichiometry in a system shares a score. Results paragraph R3 depends on the reader knowing this. The same is true of popularity.

### M6 — Outcomes

- **Prose:** `03-manuscript-skeleton.md:113`.
- **Verify:**
  - `src/mp_pu.jl:222-236`.
  - `docs/mp-recovery-protocol.md:162-202`.
  - System fields in `docs/evaluation-metrics.md` (§ *System-concentration fields*).

### M7 — Diagnostics (all post hoc)

- **Prose:** `03-manuscript-skeleton.md:119`, which already includes the E1 wording.
- **Verify:**
  - Subgroup and concentration: `scripts/analyze_element_pair_stability.py`, functions `subgroup_rows` and `concentration_rows`.
  - E1 definitions: the whole of `docs/paper-planning/09-e0-system-metrics-spec.md`.
  - E1 code: `scripts/analyze_matched_system_metrics.py`, functions `ranking_rows`, `random_expected_hit_systems` and `tie_fields`.
- **Add:** one sentence saying that system counting follows chemotype "first found" accounting (L9), and that effective hit systems plays the role of cluster weighting (L10).

### M8 — Software and reproducibility

- **Prose:** `03-manuscript-skeleton.md:125`.
- **Verify:**
  - Run identities at `01-repository-history.md:62-70`.
  - Checks at `08-verification.md:5-18` and the addendum at `08-verification.md:65-78`.
  - `docs/mp-pilot-reproduction.md`.
- **Add:** E1 was cross-checked between Julia and Python; the figure outputs are byte-reproducible.
- **Must say:** exact reproduction with the real data depends on data access (see *End matter*).

---

## Results (about 1,200 words)

Put the denominators first, then paired effects, then system coverage, then stability.

### R1 — Two holdouts build different tasks → Table 1

- **Prose:** `03-manuscript-skeleton.md:133`.
- **Table:** `t1-populations.md`, with full precision in `t1-populations.tsv`.
- **Numbers:**
  - Composition/original: N = 8,218 and h = 1,071; random expectation at K=100 is 13.03.
  - System/original: mean N = 2,513.55 [2,359–2,710] and h = 1,071.80; random expectation 42.65.
- **Must say:** raw hit counts cannot be compared across designs.

### R2 — Ordering depends on policy, design and budget → Figure 1, Table 2, Figure S1, Table S1

- **Prose:** `03-manuscript-skeleton.md:139`.
- **Figures:** `f1-paired-differences.pdf`, `t2-main-outcomes.md`, `s1-all-budgets.pdf` and `s1-label-modes.md`. Per-split and per-budget values are in `f1-data.tsv` and `s1-data.tsv`.
- **Numbers (Table 2):**
  - Composition/original: similarity 13.40, popularity 12.90, pair 12.70, random expectation 13.03.
  - System/original: 29.85, 44.30 and 52.25, against a random expectation of 42.65.
  - Pair − popularity in system holdout: +7.95 (13/2/5), +1.35 (12/2/6), +2.15 (12/1/7).
  - Similarity − popularity in system holdout: −14.45, −19.70, −15.20, negative in 19 of 20 splits each.
- **Budget reversals (`s1-data.tsv`):** composition/original similarity − popularity is −1.85 at K=20, +0.50 at K=100 and −0.35 at K=200.
- **Tie caveat:** add one sentence saying that small margins sit within cutoff-tie ranges. The source is `10-e1-system-metrics-results.md:60-68`, with values in `reports/local/matched-system-metrics-2026-09-22/tie-sensitivity.tsv`. Example: pair − popularity under exclude-mixed spans −2.00 to +4.20 depending on tie order.

### R3 — Composition hits versus systems reached → Figure 2

This is the paper's most distinctive result. Present it carefully.

- **Prose to adapt:** `03-manuscript-skeleton.md:145`.
- **Order of the paragraph:**
  1. The subgroup totals (17, 24 and 22 system-disjoint hits vs 42.13, 45.04 and 38.53 expected; `reports/local/element-pair-diagnostics-stability-2026-09-07/analysis/subgroup-summary.tsv`).
  2. The pre-stated primary contrast and its reading "extends" (`10-e1-system-metrics-results.md:21-31`).
  3. The coverage table: pair 6.2–11.1 positive systems vs similarity 20.2–23.8 vs 30.1–39.4 expected at random (`10-e1-system-metrics-results.md:35-48`).
  4. Budget dependence (`10-e1-system-metrics-results.md:50-58`).
- **Figure:** `f2-system-coverage.pdf`, with source data in `reports/local/matched-system-metrics-2026-09-22/system-metrics-by-split.tsv`.
- **Must say:**
  - The analysis is post hoc.
  - Systems are element sets, not chemical diversity.
  - The low counts for the two system-level scorers are partly built into how they score (`10-e1-system-metrics-results.md:80-84`).
- **Don't:** claim the pair model is "better at systems". It beats popularity by 1–3 systems and trails similarity by about 15.

### R4 — Recommendations shift more than mean hits → Figure 3

- **Prose:** `03-manuscript-skeleton.md:151`.
- **Figure:** `f3-optimization-stability.pdf`.
- **Numbers** (`reports/local/element-pair-diagnostics-stability-2026-09-07/analysis/stability-summary.json`):
  - 101 of 120 primary fits were capped, and all 120 converged by iteration 11,309.
  - 55 of 101 capped top-100 sets changed, with up to 48 replacements; none of the 19 converged sets changed.
  - Mean Δ hits was +0.16, ranging from −5 to +4.
- **Must say:** the 2,000-iteration result remains primary.

### R5 — Verification (optional in the main text)

To save words, fold this into M8 or the supplement.

- **Prose:** `03-manuscript-skeleton.md:157`.
- **Numbers:** 1,472 and 992 file hashes; 11 analysis files reproduced byte for byte (`08-verification.md:9-12`); E1 inventory of 842 files (`08-verification.md:71`).

---

## Discussion (about 800 words, exactly three arguments)

### D1 — Evaluation design decides what a result can claim

- **Start from** `03-manuscript-skeleton.md:165`. It needs only light edits.
- **Add comparisons:**
  - Chung's label-scheme dependence parallels RQ1 (`11-l1-nearest-work.md:16`).
  - Li's finding that nominal out-of-distribution splits are interpolation, and Meredig's leave-one-cluster-out results, parallel the design confound.
- **Use:** the reversal sentence at `02-evidence-and-framing.md:62`.
- **Limitations belong here:** one snapshot; oxygen-containing ternaries; simple methods; no chronological holdout, unlike SynthNN and Ogoshi (`11-l1-nearest-work.md:36`).

### D2 — The useful unit may be coarser than a composition row

**Rewrite this from scratch.** The provisional text at `03-manuscript-skeleton.md:171` predates E1, and its "until references are evaluated identically" sentence is now resolved.

- **New argument:**
  - Composition Hits@K credits scorers that are constant within a system for filling the budget with whole systems.
  - At the same budget, similarity reaches about 2–4 times as many positive systems.
  - Recommend reporting hit systems and effective hit systems alongside Hits@K, heeding the warning about "first found" counting in Mackey & Melville (L9) and the weighting in Clark & Webster-Clark (L10). Recommender-systems coverage (L11) is the general frame.
- **Limits:**
  - Element sets are not structural or functional diversity.
  - Popularity and the pair model cannot separate stoichiometries within a system.
- **Future work:** a system-level endpoint (`06-parking-lot.md`, "System-level endpoint" row). State it as future work, not as done.

### D3 — Reproducibility and stability are necessary but not sufficient

- **Start from** `03-manuscript-skeleton.md:177`. It is close to final.
- **Draw on:** Figure 3 and R4 for stability; the tie ranges add a second example of fragility in the recommendations.
- **Close restrained:** end on what would justify stronger chemical claims (audited labels, new data, prospective design).

---

## Abstract (write last; 180–220 words)

- **Start from** `03-manuscript-skeleton.md:25`, but replace the concentration sentence ("…only 5.68 effective systems…") with the E1 comparison.
- **Structure** (budget at `03-manuscript-skeleton.md:21`):
  1. Problem (≈30 words).
  2. Setting (≈55).
  3. Findings (≈80): the reversal across designs; pair +7.95 over popularity in system/original; the system-coverage contrast (6–11 vs 20–24 vs 30–39); 55 of 101 capped lists changed while mean Δ was +0.16.
  4. Scope (≈35).
- **Check:** every number in the abstract must appear in the Results.

## End matter

- **Data and code availability:** not written yet (`03-manuscript-skeleton.md:181`).
  - Needs backlog tasks D1 and V1 (`05-backlog-and-decisions.md`).
  - The aggregate tables and figures may be shared with MP attribution (`docs/publication-permissions.md:54`); row-level rankings may not, without review.
  - Name the software version: the `v0.1.1` tag plus the commits that added E1 and the figure script.
- **Contributions:** as sole author, one CRediT statement.
- **References:** only L1–L15 as verified (`07-literature.md:7-26`), plus the leads at `07-literature.md:32-42` once you have read them.
- **Supplement:**
  - Figure S1 and Table S1.
  - E1 tables at all budgets (`reports/local/matched-system-metrics-2026-09-22/report.md`).
  - Tie sensitivity.
  - Protocol chronology (`01-repository-history.md:44-60`).
  - Verification record (file 08).

## Final checks before sharing the draft

1. Re-derive every number from these tables:
   - `t1-populations.tsv` and `t2-main-outcomes.tsv`
   - `f1-data.tsv` and `s1-data.tsv`
   - `reports/local/matched-system-metrics-2026-09-22/system-metrics-summary.tsv`, `paired-differences.tsv` and `tie-sensitivity.tsv`
   - `stability-summary.json` and `subgroup-summary.tsv`
2. Captions carry the MP attribution and transformation notice (`captions.md`, checked against `docs/publication-permissions.md`).
3. Close the literature open items (`11-l1-nearest-work.md:57-62`): Chung and SynthNN supplements, a SynCoTrain read, the Jang lead.
4. Search the draft for these words: "significant", "first", "discover", "synthesizab", "precision", "leak", "mechanism", "better". Each occurrence must survive the rules table above.
5. Optionally, ask a trusted reader to follow `docs/mp-pilot-reproduction.md` in a fresh directory (backlog task R1) before submission.
