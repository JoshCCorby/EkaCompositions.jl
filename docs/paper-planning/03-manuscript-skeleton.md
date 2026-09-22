# Annotated manuscript skeleton

**Status:** provisional draft, assembled Methods → Results → Introduction → Discussion → Abstract. Reading order below is conventional IMRaD. Numbers are from retained experiments; the investigation reproduced saved-data analysis, not fresh model fits. Bracketed `MISSING` items are unfinished work, never anticipated findings.

**Article type:** short empirical methods/evaluation study, accompanied by research software. **Audience:** researchers building or evaluating inorganic-composition ranking systems; materials-informatics reviewers interested in benchmark validity. **Provisional main-text budget:** 3,500–4,500 words excluding references and detailed protocol supplement.

**Preferred working title:** *What composition-recovery benchmarks measure: label and holdout sensitivity in oxygen-containing ternaries*

**Alternatives:**

1. *From composition hits to chemical systems: an audit of materials-recovery rankings*
2. *Evaluating inorganic-composition rankings with provenance labels and grouped holdouts*
3. *EkaCompositions: a reproducible case study of positive–unlabelled materials recovery*

**One-sentence thesis:** In a fixed Materials Project snapshot, label policy and holdout design change the apparent benefit of composition-ranking methods, while system concentration and optimization sensitivity constrain the interpretation of their recovered hits.

**Research questions:** RQ1, how sensitive are within-pool method comparisons to label policy and holdout design? RQ2, how much apparent composition recovery represents coverage of distinct chemical systems? RQ3, how stable are recovered counts and individual recommendations to the declared optimization budget?

## Abstract — draft last, read first

Target 180–220 words: context/problem 30; setting/methods 55; measured findings 80; interpretation/scope 35. Annotation A1: topic is the bounded finding; role is to make the endpoint and strongest evidence unmistakable; sentence topics are provenance recovery, six evaluation branches, conditional rankings, concentration, optimization stability and scope. Evidence: C3–C8, figures F1–F3. E1 complete (file 10): state the small margin over popularity only together with the much lower system coverage than similarity or random; no system-level superiority claim.

**Provisional abstract, drafted after Methods, Results, Introduction and Discussion:**

Composition-ranking benchmarks often recover database labels whose relationship to experimental synthesis is indirect. We examine how evaluation choices affect such recovery using a fixed Materials Project snapshot of oxygen-containing ternaries. The study compares random ranking, training-element popularity, maximum composition cosine similarity and a rank-four nonnegative element-pair model across two holdout procedures, three provenance-label policies and 20 deterministic overlapping partitions. Under the original policy, similarity and popularity recover 13.40 and 12.90 positives at a budget of 100 compositions in composition holdout; under system holdout they recover 29.85 and 44.30. The pair model averages 52.25 hits in the latter task, but the corresponding random expectation is 42.65 and its positive hits represent only 5.68 effective systems on average. A later optimization-cap analysis changes 55 of 101 previously capped top-100 sets, with up to 48 replacements, while mean hit change is only +0.16. These findings show that method ordering, clustered recovery and recommendation stability require separate reporting. The two holdout procedures also change candidate populations, precluding a causal attribution to chemical separation. Results concern withheld provenance labels in one snapshot, not prospective discovery or synthesis success. Reproducible software and retained run records support inspection; public exact reproduction additionally depends on access to the real input artifacts.

## Introduction

### I1. Composition recommendation and the broader problem

**Role:** establish why ranking is useful without promising synthesis from a formula.

**Sentence topics:** (1) Large inorganic composition spaces motivate prioritization. (2) Database-informed recommenders offer one route. (3) Materials databases mix observed and computational records. (4) Database presence and provenance are not identical to experimentally realizable chemistry. (5) Evaluation must identify which endpoint is being recovered.

**Evidence/citations:** Seko et al. [L1](07-literature.md); Jain et al. [L2](07-literature.md); dataset definition M1/M2. **Unresolved:** no assertion about laboratory cost or total chemical-space size needs an unsupported number.

**Provisional topic sentence:** Composition-level recommendation can prioritize inorganic candidates, but its evaluation depends on what a database label represents.

### I2. Prior approaches and evaluation targets

**Role:** situate the work among existing recommender and PU studies.

**Sentence topics:** (1) Matrix/tensor recommenders have already been proposed. (2) Composition-based and structure-based synthesizability methods have different inputs and endpoints. (3) PU approaches acknowledge absent confirmed negatives. (4) Chemical-system familiarity and labeling bias have already been discussed. (5) An apparent new-system test need not be extrapolation in representation space. (6) Those precedents motivate a focused diagnostic study, not a claim to invent PU evaluation.

**Evidence/citations:** L1, L3–L5; leads in file 07 require full-text verification before specific comparison. **Unresolved:** complete L1 task's closest-paper matrix; do not compare published headline scores to Eka's Hits@100.

### I3. The specific gap to investigate

**Role:** turn established concerns into a bounded research question.

**Sentence topics:** (1) A fixed row budget can reward repeated stoichiometries within one element set. (2) Alternative label rules change training and candidate populations. (3) Holdout construction changes both proximity and prevalence. (4) Stable average hits can coexist with unstable selected candidates. (5) These issues should be examined jointly with retained rankings and explicit provenance. (6) Whether this combination is sufficiently distinct is a contribution question, not an assumed literature gap.

**Evidence/citations:** C3/C7/C8; `src/element_pair_model.jl:119–136`; literature comparison. **Unresolved:** replace “few studies” or “first” language with an exact contrast supported by reviewed papers.

### I4. Question and supported contributions

**Role:** state precisely what the paper delivers.

**Sentence topics:** (1) Introduce RQ1–RQ3 in one sentence. (2) Define one MP snapshot and oxygen-containing ternaries. (3) State two holdouts, three policies, four rankers and fixed budgets. (4) Offer conditional empirical comparisons. (5) Offer system/convergence diagnostics and inspectable software. (6) Exclude prospective discovery, calibrated synthesis probability, causal separation effects and state-of-the-art superiority from the claimed contribution.

**Evidence:** M1–M8, R1–R5, C1–C9. **Unresolved:** decide whether a short technical report is the right scale after closest-work review.

## Methods — initial rough prose

### M1. Study setting and source snapshot

**Role:** define the population before describing models. **Sentence topics:** one snapshot; version/retrieval; query; retained chemistry; composition versus structure; no chronology. **Evidence:** `data/local/mp-ternary-snapshot/snapshot.toml`; `docs/mp-recovery-protocol.md:13–42`; L2. **Unresolved:** finalize data-availability wording, not new data acquisition.

**Provisional prose:** We evaluated recovery of withheld experimental-provenance labels within one Materials Project snapshot (database version 2026.04.13), retrieved on 31 August 2026 at 12:16:39 UTC using mp-api 0.46.5. The recorded query selected non-deprecated entries containing oxygen and exactly two other elements and set `include_gnome=false`. Hydrogen- and halogen-containing compositions were retained. We describe this population as oxygen-containing ternaries because element membership alone does not validate oxide chemistry or oxidation states. The study's unit was a reduced composition rather than an individual crystal structure. Snapshot timestamps were not interpreted as discovery dates.

### M2. Canonicalization and provenance policies

**Role:** define the evaluation unit and endpoint; explain why label sensitivity matters. **Sentence topics:** exact integer parsing; ratio reduction; group all records; original positive/unlabelled rule; alternate mixed policies; endpoint limits. **Evidence:** `src/mp_audit.jl:184–227`; `src/mp_label_sensitivity.jl:14–38`; frozen label-sensitivity protocol. **Unresolved:** no independent chemical truth audit exists; report this explicitly.

**Provisional prose:** Formula normalization combined repeated element symbols, reduced positive integer amounts by their greatest common divisor and sorted element symbols into a canonical representation. All records with an equivalent reduced composition were grouped before constructing splits, preventing different polymorphs or proportional formula spellings from appearing as separate train and test compositions. Under the original policy, a group was positive if any member record explicitly had `theoretical=false`; groups with only true flags were unlabelled, while unresolved groups were excluded. Two additional policies respectively removed groups with both true and false flags or treated those groups as unlabelled. We rebuilt the training and candidate populations for the main comparisons under each policy. The labels represent database provenance rather than literature-audited synthesis outcomes, and unlabelled compositions were never treated as confirmed failed syntheses in evaluation.

### M3. Holdout construction

**Role:** distinguish two target tasks and expose changed denominators. **Sentence topics:** formula fifth; all unlabelled candidates; common system universe; selected systems; unused outside-system unlabelled; noncausal contrast. **Evidence:** `src/mp_recovery.jl:63–99`; `src/mp_system_holdout.jl:18–50`; v1/v2 protocols. **Unresolved:** none for describing executed procedure; a matched-pool causal study is future work.

**Provisional prose:** Composition holdout selected floor(P/5) positive compositions for evaluation, where P is the policy-specific positive count; remaining positives formed the training set and all eligible unlabelled compositions joined the held-out positives as candidates. Chemical-system holdout instead selected floor(S/5) systems from a common universe defined before policy filtering, where a system is an unordered element set. Training then contained only positives outside the selected systems, and candidates contained the eligible positive and unlabelled compositions within them. Unlabelled compositions outside the selected systems were unused. Both designs used the 20 predeclared split seeds 0–19 and versioned SHA-256 ordering, with disjointness checked after reconstructing memberships. Because the designs change candidate membership, prevalence and training composition, their contrast does not isolate a causal effect of chemical separation.

### M4. Reference rankings and input isolation

**Role:** give reproducible baseline definitions. **Sentence topics:** popularity equation; cosine equation; random keys; label isolation; ties; external-score exclusion. **Evidence:** `src/mp_pu.jl:125–210`; `docs/mp-external-score-provenance.md`; L1. **Unresolved:** independent Python baseline similarity arithmetic is not a full raw-input refit; distinguish verification levels in M8.

**Provisional prose:** Element popularity scored a candidate by the mean fraction of training compositions containing each of its elements, with each canonical composition counted once. Maximum similarity scored a candidate by the greatest cosine overlap of its reduced element-count vector with a training composition. The random reference used a versioned hash ordering with ranking seed 10000 plus the split seed, and its analytical comparator was uniform sampling without replacement. Rankers received only training and candidate compositions; evaluator-owned labels were attached after ranking. Exact score ties were resolved by a shared formula hash with tie seed 20260901, followed by canonical formula order. Released Seko scores were excluded because their training independence was not established and their coverage differed by label; the exclusion makes no statement about their accuracy on the upstream task.

Let T be the training set, E(c) the candidate's elements, and n(e) the number of training compositions containing e:

\[
s_{pop}(c)=\frac{\sum_{e\in E(c)}n(e)}{|E(c)|\,|T|},\qquad
s_{cos}(c)=\max_{t\in T}\frac{c\cdot t}{\|c\|\,\|t\|}.
\]

### M5. Fixed element-pair comparator

**Role:** describe the method sufficiently to interpret its ties and limits; do not market it as a new factorization family. **Sentence topics:** pair counts; target; weighted objective; settings; score/cold rule; consequences of omitted stoichiometry. **Evidence:** `src/element_pair_model.jl:11–72,87–136`; frozen pair protocol; L6/L7. **Unresolved:** missing-pair ablation and rank/restart sensitivity are not completed experiments.

**Provisional prose:** The learned comparator represented each oxygen-containing ternary by its pair of non-oxygen elements. Each distinct training composition incremented its unordered pair count C_ab once, and the target was Y_ab=log(1+C_ab)/log(1+|T|). We fit a rank-four nonnegative factor matrix over the 117 non-oxygen elements, using weight 1 for observed pairs, weight 0.01 for missing pairs and regularization 0.01. Optimization used deterministic initialization seed 20260902 and projected gradient with Armijo backtracking, a projected-gradient stopping tolerance of 10⁻⁴ times max(1, initial residual), and a primary cap of 2,000 iterations. A candidate's score was the dot product of its two factor rows; candidates with unseen training elements received zero and a coverage flag. Consequently all stoichiometries in a chemical system shared a score, while the weak zero targets encoded an association-model assumption rather than verified negative compounds or an unbiased PU learning objective.

\[
\min_{F\geq0}\frac12\sum_{a<b}w_{ab}(F_a^\top F_b-Y_{ab})^2+
\frac{0.01}{2}\sum_{a,k}F_{ak}^2.
\]

A finite state at the iteration cap was permitted by the frozen protocol and retained as the primary fixed-compute result. Meeting the stationarity criterion is not a proof of a global optimum.

### M6. Outcomes and descriptive comparison

**Role:** align metrics with the endpoint and avoid pseudoreplication. **Sentence topics:** primary K; secondary cutoffs; metric denominators; pair differences; descriptive split variability; no negative-class performance. **Evidence:** `src/mp_pu.jl:222–236`; v1/v2/pair protocols. **Unresolved:** if inferential uncertainty is requested later, define its target/sampling unit first.

**Provisional prose:** The primary outcome was the number H_K of deliberately held-out positive compositions recovered among the first K=100 candidates, with K=20, 50 and 200 reported as secondary budgets. For candidate count N and held-out-positive count h, we also reported H_K/K, H_K/h and enrichment (H_K/K)/(h/N), alongside the uniform-random expectation Kh/N. Primary comparisons used similarity-minus-popularity for the reference study and pair-minus-popularity for the added comparator, computed within each identical branch and split. We retained all 20 paired differences and summarized their mean, median, range and positive/zero/negative counts. These overlapping holdouts measure sensitivity to the chosen partition rather than independent experimental replication. Observed-label fraction is not synthesis success or precision measured against confirmed negatives.

### M7. Label, system and optimization diagnostics

**Role:** label chronology and distinguish completed analyses from planned ones. **Sentence topics:** label modes; same-system subgroup; concentration indices; cap sensitivity; primary preserved; missing matched all-method analysis. **Evidence:** `scripts/analyze_element_pair_stability.py:26–130`; label-sensitivity protocol; `0629ba9`. **Resolved by E1 (file 10):** specification written before computing (file 09) and identified as post hoc.

**Provisional prose:** The earlier label-sensitivity workflow distinguished evaluation-only relabelling of fixed rankings from full-pipeline rebuilding of training, candidates and labels. The principal design comparison used the full-pipeline branches. Later exploratory diagnostics counted system-disjoint held-out positives within composition holdout and the number and concentration of systems represented by the pair model's top-100 hits. For system s with h_s hits, effective hit systems were defined as H²/Σ_s h_s², alongside distinct selected systems, distinct hit systems and largest hit share. A post-hoc optimization study changed only the iteration cap from 2,000 to 20,000 and compared stopping states, top-100 set replacement and hit changes; the original fixed-compute results remained primary. A further post-hoc analysis, specified before computation, applied the same system metrics to all four saved rankings on identical held-out sets at every budget. It added system recall, an exact uniform-random expectation of hit systems, and the range of Hits@K achievable by reordering only score ties that cross the cutoff. No ranking was recomputed. [Provisional wording from E1, file 10.]

### M8. Software, provenance and reproducibility

**Role:** distinguish identity, saved-data verification and rerunning. **Sentence topics:** Julia/Python; frozen bytes; dirty overlays; historical rerun; present audit; availability limits. **Evidence:** file 01 run-identity table; file 08; `docs/mp-pilot-reproduction.md`; `scripts/analyze_element_pair.py:42–134`. **Unresolved:** final reviewer-access package and archive DOI/version identity.

**Provisional prose:** EkaCompositions implements the ranking and evaluation workflows in Julia, with separate Python analyzers for independent reconstruction of memberships, metrics and factor-derived scores. Each retained run records protocol, source, implementation and deterministic-output hashes together with its execution configuration and environment. Experiments executed from modified working trees retain source archives and patches in addition to their base commit, so a commit identifier alone is not their complete implementation identity. Historical reproduction records report separate-checkout reruns and refits using the preserved Julia 1.12.6 environment and an existing package depot. For this manuscript-planning audit, we checked saved output inventories and reran the factor-based diagnostic analysis, obtaining byte-identical analysis outputs; we did not independently refit the models. The source repository exposes synthetic workflows, while exact real reproduction additionally requires the retained snapshot and baseline artifacts, whose final availability remains to be specified.

## Results

### R1. The two holdouts construct materially different recovery tasks

**Role:** put denominators before headline hits; addresses RQ1. **Sentence topics:** records collapse; original P/U; mixed flags; original formula pool; original system mean pool; cross-design comparability. **Evidence:** saved audit; system `analysis/populations.tsv` and `method-summary.tsv`; T1. **Unresolved:** E2 should add full system-universe count, ranges and all training denominators from saved population tables.

**Provisional result:** The snapshot contained 24,020 records representing 12,506 reduced compositions, of which 5,359 were originally positive and 7,147 unlabelled. Mixed provenance occurred in 1,343 positive groups. Original-policy composition holdout used 8,218 candidates and 1,071 held-out positives per split. Original-policy system holdout averaged 2,513.55 candidates and 1,071.80 positives, producing a mean random top-100 expectation of 42.65 rather than 13.03. The larger raw hit counts under system holdout therefore cannot be interpreted without the changed candidate population.

### R2. Method ordering and margins depend on policy, design and budget

**Role:** answer RQ1 with paired effects rather than a leaderboard. **Sentence topics:** original cosine small advantage; alternate-policy changes; system reversal; pair margins; signs/variation; budget sensitivity. **Evidence:** C3–C5; pair/system `analysis/summary.tsv`; F1, T2 and S1. **Unresolved:** render all split dots and secondary-budget panel from saved tables.

**Provisional result:** At K=100 under original-policy composition holdout, similarity recovered 13.40 positives on average, popularity 12.90 and the pair model 12.70, against a random expectation of 13.03. Under system holdout, the corresponding means were 29.85, 44.30 and 52.25, against 42.65 expected at random. Pair-minus-popularity differences were +7.95, +1.35 and +2.15 for the original, exclude-mixed and unlabel-mixed system policies, respectively. The original-policy advantage was positive in 13 splits, zero in two and negative in five. These are conditional descriptive comparisons; for example, original-policy composition similarity-minus-popularity was −1.85 at K=20 and −0.35 at K=200. No significance or universal method ranking is inferred.

### R3. Composition hits do not directly count distinct successful systems

**Role:** answer the supported portion of RQ2 and make missing comparative evidence visible. **Sentence topics:** system-disjoint share; sparse event totals; uniform expectation; selected/hit/effective systems; large tie blocks; all-method placeholder. **Evidence:** C6/C7; post-hoc analysis regenerated in file 08; F2. **Unresolved:** none from E1; F2 assembly remains.

**Provisional result:** Across the overlapping composition holdouts, the pair model recovered 17, 24 and 22 system-disjoint positive appearances at K=100 under the three policies, compared with random expectations of 42.13, 45.04 and 38.53. These totals do not count unique discoveries. In original-policy system holdout its top 100 contained a mean of 13.5 distinct systems, with positive hits from 9.0 systems and 5.68 effective hit systems. One system occupied as many as 52 rows in a top-100 list. On the identical system-holdout pools, the pair model reached 1.15–2.80 more positive systems than popularity on average across policies. Popularity and the pair model reached 6.2–11.1 positive systems, compared with 20.2–23.8 for similarity and 30.1–39.4 expected under uniform random selection. Composition hits and system coverage therefore order the methods differently. [Provisional wording from E1, file 10; retain the budget and tie-order caveats.]

### R4. Recommendation identities are more sensitive than mean hits to the iteration cap

**Role:** answer RQ3; separate numerical robustness from better scientific prediction. **Sentence topics:** capped primary fits; longer-run stationarity; changed capped lists; unchanged converged lists; replacement versus hits; no promotion of later result. **Evidence:** C8; `stability-by-fit.tsv`, `stability-summary.json`; F3. **Unresolved:** no independent initialization/rank assessment; not required for the bounded cap-sensitivity finding.

**Provisional result:** The primary run reached its iteration cap in 101 of 120 fits. In the later 20,000-iteration run, all fits met the same stationarity criterion by iteration 11,309. Top-100 sets changed for 55 of the 101 previously capped fits, with up to 48 replacements, while none of the 19 previously converged sets changed. Hit differences averaged +0.16 and ranged from −5 to +4. This supports a distinction between aggregate recovery stability and the stability of individual recommendations, without replacing the prospectively frozen primary result.

### R5. Verification supports local inspectability, with an availability boundary

**Role:** establish the evidence chain without equating software tests with chemistry. **Sentence topics:** preserved configs; inventories; fresh analysis equality; historical refit report; public synthetic path; remaining access gap. **Evidence:** file 08 and run-identity table; T2 footnote or supplement. **Unresolved:** data release/access decision before submission.

**Provisional result:** This investigation verified 1,472 system-holdout and 992 primary pair deterministic file hashes. Reanalysis of the saved primary and stability runs reproduced all 11 retained diagnostic-analysis files, including their inventory, byte for byte. The full model refit and clean-checkout equality remain historical results recorded in the bundles rather than experiments repeated here. Exact external reproduction still depends on access to the retained real inputs.

## Discussion — at most three central arguments

### D1. Evaluation design determines the claim a recovery result can carry

**Role:** interpret RQ1 and compare with relevant literature. **Sentence topics:** changed ordering; label proxy sensitivity; task distributions confound causal separation; relation to Li and PU work; scope of snapshot recovery; implication for reporting. **Evidence:** R1/R2, L3/L4, M2/M3. **Unresolved:** closest-work paragraph must use verified full-text distinctions.

**Provisional paragraph start:** The variation across these recovery tasks shows why a ranking result should be reported together with its label rule and candidate population. The similarity reversal is consistent with dependence on shared-system proximity, but it does not isolate that mechanism because the holdout procedures also change the pools. Prior work already cautions that nominal chemistry holdouts can remain interpolative; the present case adds a fixed-budget provenance-recovery example rather than a general solution to materials extrapolation. Applicability is limited to this snapshot, chemistry scope and set of simple methods.

### D2. The useful unit of recommendation may be coarser than a composition row

**Role:** interpret RQ2; include study limitations and the most valuable next analysis. **Sentence topics:** within-system ties; clustered hits; effective index is not sample size; compare all methods before superiority; raw-pair/missing-weight future work only if method claim; implications for user budgets. **Evidence:** R3, M5/M7; E1; standard symmetric factorization lineage L6. **Unresolved:** no evidence that selected-system count itself predicts chemical utility.

**Provisional paragraph start:** A top-100 composition list is not necessarily 100 distinct chemical-system choices. The element-pair representation makes this explicit because all stoichiometries within a system receive the same score. Concentration diagnostics expose how a favorable composition hit count can be supported by relatively few systems, but they do not establish that the comparator is worse or better at useful system coverage until references are evaluated identically. Nor does element-set diversity measure structural or functional diversity. The immediate next step is comparative system-aware evaluation, rather than expanding model capacity.

### D3. Reproducibility and optimization stability are necessary but insufficient for scientific usefulness

**Role:** connect RQ3 and software evidence to measured scope; contain future work and restrained closing. **Sentence topics:** deterministic primary procedure; cap sensitivity; numerical stationarity versus truth; one snapshot/label limitations; independent input/label validation and availability; restrained close. **Evidence:** R4/R5, L7, verification record. **Unresolved:** final artifact availability and any independently adjudicated labels.

**Provisional paragraph:** Preserving complete rankings and optimization traces made it possible to distinguish stable average recovery from changing individual recommendations. This distinction matters when a model is used to select a short list, even though the longer optimization run did not constitute a new prospectively selected method. Exact computational reproduction cannot validate the provenance proxy, remove research-frequency bias, establish synthesis success or prove a global optimum. Broader claims would require independently audited outcomes and additional data or prospectively designed evaluation settings. The immediate contribution is therefore a transparent, limited account of what this recovery experiment measures and the evidence needed before its rankings can support stronger chemical conclusions.

## End matter placeholders

**Data/code availability:** [MISSING: accessible artifact inventory, permitted contents, immutable source identity, reviewer restore instructions; do not assert public availability from local existence]. **Contributions:** [co-authors to agree actual CRediT roles and order]. **Affiliations, funding, competing interests, acknowledgments:** [to be supplied and verified; none inferred]. **References:** use verified register in file 07; search leads are not ready bibliography entries. **Supplement:** all budgets, split differences, population ranges, score/tie/cold-element diagnostics, protocol chronology and reproduction scope.
