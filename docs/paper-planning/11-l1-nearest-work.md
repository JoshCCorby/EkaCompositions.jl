# L1 — Nearest-work comparison and C15 novelty check

Read 22 September 2026. This was a focused search, not a systematic review, and it does not show that anything is absent from the literature. **No supplementary material (ESI) was read for any paper.** Every "not reported" below means only "not found in the text inspected".

How each source was read:

- **Read directly:** Chung, SynthNN and Seko 2018 (full main text, extracted to text); Hayashi 2022 (full text); Mackey & Melville, Clark & Webster-Clark and Kaminskas & Bridge (abstracts).
- **Summarised by an automated page reader:** Li, SynCoTrain and Ogoshi. Confirm their specifics by a human read before citing them.
- **Metadata or search results only:** Meredig, Borg, Adomavicius & Kwon, and Hayashi & Tanaka 2025.

## Comparison with the closest materials work

| Work | Endpoint and data | Unit and representation | Split / grouping | Metric | Label-policy sensitivity | System-level coverage of hits |
| --- | --- | --- | --- | --- | --- | --- |
| **Eka** | Withheld MP experimental-provenance flag; O-containing ternaries, one 2026 snapshot | Composition; element sets, popularity, max cosine, rank-4 pair factorization (constant within a system) | Composition groups vs whole-system holdout, 20 hash splits | Hits@K (20–200), enrichment, exact random expectation | 3 mixed-label policies × 2 designs | **Yes (E1):** hit systems, system recall, effective hit systems, tie ranges |
| Chung, Walsh & Payne 2025 (L4) | Human-curated solid-state synthesis labels for MP ternary oxides (MP 2020-09-08 with ICSD IDs); 2,213 positive / 508 non-solid-state / 4,312 hypothetical (§2.1, §2.3) | Composition; matminer and melting-point features, bagged decision-tree PU (§2.3–2.4) | 10-fold cross-validation repeated 10×; no chemical-system grouping stated (§2.4) | ROC AUC, G-mean, TPR/FPR (§2.5) | **Yes:** model 1 vs 2 changes only how non-solid-state compositions are labelled; AUC 0.921 vs 0.771 (§3.5.1, Table 3) | **Partial:** 141/168 (83.9%) of predicted positives lie in systems with a training positive (§3.5.4). This is familiarity, not coverage |
| Antoniuk et al. 2023, SynthNN (L5) | ICSD compositions (53,594 binary to quaternary) vs artificially generated formulas at a 20:1 ratio (Methods) | Composition; learned atom embedding, deep network | Random 90:5:5 split, plus **decade-by-decade chronological holdout** (Fig. 4) | Precision, recall, F1; vs charge-balancing, Roost, 20 human experts | Semi-supervised reweighting; no label-policy comparison found | No; breakdown by element family and by number of elements (Fig. 3) |
| Amariamir, George & Benner 2025, SynCoTrain (L8)\* | **MP experimental vs theoretical oxides**, a label close to Eka's endpoint; 10,206 positive / 31,245 unlabelled | Crystal structure; ALIGNN and SchNet co-training | Random positive holdouts (10% varying, 5% fixed); no grouping reported | Recall on held-out positives; predicted-positive rate | Not reported | Not reported |
| Seko et al. 2018 (L1) | ICSD compositions as known; test set = ICDD and SpringerMaterials entries absent from ICSD | Composition; tensor over cations, anion and **integer stoichiometry set**, so scores vary within a system | External-database holdout | Discovery rate in the top 100 and top 3,000 vs random (0.056%) | Not applicable | Not found |
| Hayashi, Seko & Tanaka 2022 (review) | Same programme; also descriptor-based recommender and synthesis-condition tensor | Composition | External-database holdout | Discovery rate in the top N | — | Not found; the phrase "chemical system" does not appear in the text |
| Ogoshi et al. 2023\* | OQMD v1.4 → v1.5 new stable compounds | Ion-to-site bipartite graph (not element pairs) | **Chronological (database version)** | Precision of recommendations vs brute force (31.5% vs 11.6%, halide perovskites) | — | Not reported |
| Li et al. 2025 (L3)\* | Formation-energy regression; JARVIS, MP, OQMD | Structure and composition models | Leave-one-element, period, group or symmetry out | MAE, R² | — | Not applicable; shows most nominal OOD tasks are interpolation |
| Meredig et al. 2018 (metadata and search results only) | Superconductor Tc | Composition | **Leave-one-cluster-out cross-validation**; clustered data inflates apparent performance | Regression and discovery | — | Addresses clustering in the *split*, not in the *metric unit* |

\* Automated summary; confirm before citing specifics.

## What Eka shares and where it actually differs

- **Shared and not new:** composition-only PU recovery (L4, L5); matrix/tensor recommender for compositions (L1); dependence on label scheme (L4 model 1 vs 2); chemical-system familiarity bias in predictions (L4 §3.5.4); clustered data inflating evaluation (Meredig; L3). A near-identical MP experimental/theoretical endpoint exists in SynCoTrain (L8).
- **Actual differences found in the inspected text:**
  1. Eka crosses three mixed-label policies with two holdout designs on one fixed snapshot, comparing within identical pools.
  2. It reports fixed-budget recovery with exact random expectations at four budgets.
  3. It measures positive **system coverage and concentration** of hits for every method (E1).
  4. It checks cutoff-tie sensitivity and the effect of the optimization budget on individual recommendations.
  5. It keeps a hash-bound evidence trail.
- **What Eka lacks and others have:** a chronological holdout (SynthNN, Ogoshi); an external-database holdout (Seko); human-curated labels (Chung); external validation such as DFT, synthesis or expert comparison (Seko, Hayashi, SynthNN).

## C15 novelty check: composition hits versus system coverage

**The principle is established in neighbouring fields.**

- **Virtual screening.** Clark & Webster-Clark (2008) weight each active inversely to the size of its series, because analogue clusters bias ROC enrichment. Mackey & Melville (2009) compare "cluster averaging" with "first found" chemotype counting. They warn that "first found" has drawbacks when combined with quantitative metrics. Eka's hit-system count is the "first found" protocol with element sets as chemotypes, and its effective hit systems plays the role of a cluster-weighted index.
- **Recommender systems.** Coverage and aggregate diversity are standard beyond-accuracy objectives that can trade off against accuracy (Adomavicius & Kwon 2012; Kaminskas & Bridge 2016).

**In the materials composition-recovery work inspected, no paper reports system coverage of held-out hits.** Chung's familiarity statistic is the closest. It measures whether predictions sit in already-known systems, which corresponds to Eka's C6, not to how many held-out positive systems are reached.

**Verdict.** C15 is not a new metric idea. It must not be framed as one, and "first" claims are ruled out. What is defensible is an application finding: chemotype-style system accounting in materials composition-recovery benchmarks reverses method orderings in system holdout. It also shows that scorers constant within a system gain from composition Hits@K by filling the budget with whole systems. Heeding Mackey & Melville, report hit systems and effective hit systems *alongside* Hits@K, never in place of it.

**Proposed contribution sentence (provisional, for C1):**

> "Using one fixed snapshot and identical candidate pools, we show that conclusions from composition-recovery benchmarks depend on label policy, holdout design and the unit counted. Borrowing chemotype-aware accounting from virtual screening, we find that the methods leading on composition hits in system holdout reach the fewest positive chemical systems."

## Effect on framing and open items

This comparison supports **framing A**, with the novelty narrowed to the controlled combination. The system-unit result is now the most distinctive element, provided it is presented with the virtual-screening and recommender-systems precedents.

Before any contribution claim is final:

1. Read the supplementary material for Chung (S1–S10) and SynthNN, and check whether either reports per-system results.
2. Confirm by a human read the SynCoTrain details marked \*; its endpoint overlaps most with Eka's.
3. Check the Jang et al. 2024 lead and Hayashi & Tanaka 2025 (*Scientific Reports* 15; DOI 10.1038/s41598-024-85062-z).
4. Run a targeted search of generative-materials evaluation, where "novelty", "uniqueness" and "diversity" rates are coverage-like but apply to generation rather than ranking.
