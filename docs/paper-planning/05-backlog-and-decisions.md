# Prioritized backlog and co-author decisions

Planning scope: complete a defensible first draft, not an indefinitely expanding benchmark. Work in 30–120 minute units. Owners below are **proposed roles, all unassigned**; they are not declarations of authorship or promises by named people. Tasks extending beyond a session should be split at the concrete checkpoint, not have their scientific scope enlarged.

## Work queue

| ID / priority / time | Concrete deliverable | Dependencies | Definition of done | Gate / proposed role |
| --- | --- | --- | --- | --- |
| A0 / done | Repository map, claim audit, IMRaD draft, storyboard, literature register, parking lot and verification record | This investigation | Eight editable planning documents plus index exist; evidence and hypotheses distinguished | First-draft foundation complete |
| E0 / **done 22 Sep** | One-page analysis specification for matched system metrics ([file 09](09-e0-system-metrics-spec.md)) | File 02 C5/C7; saved rankings | Fix all 4 methods, 6 branches, 20 splits and K=20/50/100/200; define system recall, effective hit systems and tie reporting; explicitly mark post hoc; no ranking changes | Blocks new comparative system claim / evaluation lead |
| E1 / **done 22 Sep** | Matched all-method system metric table from saved rankings ([file 10](10-e1-system-metrics-results.md): 1,920 rows, Julia/Python agreement, reading "extends" with major caveats) | E0, local artifact access | Each full ranking joins same heldout set; all 1,920 method/branch/split/budget rows present; hand-worked arithmetic and independent spot checks; factors not refit; negative results retained | Blocks completed RQ2 claim, not initial placeholder draft / analyst |
| E2 / P0 / 60–90 min | Complete T1 denominator table | Existing audit and population files | All six branches; P/U/training/candidate/holdout/system counts and ranges verified; distinguish mean ratios from ratios of means | Blocks credible Results draft / analyst |
| E3 / P0 / 90–120 min | F1 and T2 first plots, with table-to-plot checks | Saved metrics, E2 | All 240 main paired-effect dots and six branches shown; means/signs match source; original source/run identities recorded | Blocks complete first co-author draft / visualization lead |
| E4 / P0 / 60–90 min | S1 all-budget panel and label-mode summary | Existing metrics, sensitivity summaries | Include all four budgets and two modes without selectively highlighting wins; verify original K=20 and K=200 reversals | Blocks complete Results interpretation / analyst |
| L1 / P0 / 90–120 min | One-page nearest-work comparison | File 07 | Read relevant methods/evaluation sections of Li, Chung and at least one composition/PU predictor; list shared ideas, actual difference, endpoint and availability; no unverified “first” claim | Blocks contribution claim / literature lead |
| W1 / P0 / 60–90 min | Methods v0.1 with equations, chronology and run identity | M1–M8; E2 | Every procedural claim resolves to code/protocol; fixed-compute versus post-hoc explicitly separated; remove redundant annotations only after preserving them in parking lot | Blocks first draft / writing lead |
| W2 / P0 / 90–120 min | Results v0.1 anchored to F1–F3, T1/T2 and S1 | E1–E4; retained stability data | Each result uses the correct endpoint and denominator; all unresolved outcomes remain explicit; no selective cutoffs | Blocks full empirical draft / writing lead + analyst |
| W3 / P0 / 60–90 min | Introduction v0.1 and contribution paragraph | L1, W1/W2 | Four-paragraph chain matches I1–I4; novelty limited to demonstrated distinction | Blocks first draft / writing lead |
| W4 / P0 / 60–90 min | Discussion v0.1 | W2/W3 | Exactly three central arguments; limitations and future work within them; causal and discovery overclaims removed | Blocks first draft / writing lead |
| W5 / P0 / 30–45 min | Final provisional abstract and title selection | W1–W4 | 180–220 words; every finding appears in Results; no placeholders disguised as results | Last writing pass before review / writing lead |
| V1 / P0 / 45–60 min | Reproduction/availability table for review | File 08 and source archives | Mark present audit versus historical refit versus unavailable external rerun; identify data/config/command/environment for each main claim | Blocks reproducibility claim / reproducibility reviewer |
| C1 / P0 / 30–60 min | Framing and evidence checkpoint | L1, current plan | Choose A/B/C framing; record exact contribution and what will not be claimed; assign actual owners with consent | Blocks scope expansion, not independent writing / all prospective co-authors |
| F2 / P1 / 60–90 min | F2 with matched system-level references | E1 | No comparative panel remains a placeholder; shows all methods and relevant-system denominator; captions identify exploratory timing | Blocks submission if system advantage is asserted / visualization lead |
| F3 / P1 / 45–60 min | Optimization-stability plot | Regenerated diagnostics | All 120 fits accounted for; status and repeated identical fits clear; source 2k run remains primary | Needed for RQ3 presentation / visualization lead |
| R1 / P1 / 60–90 min | Independent saved-input-to-analysis reviewer walkthrough | V1, accessible retained artifacts | Reviewer follows exact commands in a new directory and documents actual boundary reached; do not claim fresh refit unless performed | Before submission / independent reviewer |
| D1 / P1 / 60–90 min | Draft artifact-specific sharing/availability inventory | Existing `docs/publication-permissions.md`; owner decision | List aggregates, raw input, memberships, factors, source and environment separately; honest route for unavailable artifacts; no automatic publication | Before external release / data steward |
| C2 / P1 / 45–60 min | First full co-author feedback meeting or written packet | Minimum review rule below | Resolve contribution, plots, unsupported sentences, missing evidence and ownership; record decisions, not unbounded rewrite requests | Review checkpoint / all authors |
| Q1 / P1 / 45–60 min | Target venue/arXiv scope note | C1, actual scope and manuscript maturity | Verify current venue/preprint scope and requirements using official pages; choose route without promising acceptance | Before submission / corresponding-author role |
| O1 / optional / 60–90 min | New-protocol direct pair-frequency integration plan | C1 chooses methods claim; dirty module inspected | Explicitly note all-zero system-holdout control; version/schema and inputs frozen before any new real comparison | Optional for recommended framing / method lead |
| O2 / optional / 90–120 min | Missing-pair-weight ablation protocol and synthetic acceptance criteria | O1; code design permitting alpha=0 | Define one scientific question, unchanged other settings, all branches and stopping rule before real execution | Not a first-draft blocker / method lead |
| O3 / optional / 60–90 min | Label-adjudication sampling plan | Chemical expertise and source access | Predefine stratified cases, independent adjudication and disagreement record; estimates only after actual review | Needed for stronger endpoint, optional for proxy paper / domain lead |
| O4 / optional / 90–120 min | Matched-pool design proposal | C1 and denominator audit | Define estimand and how train size, prevalence and pool change are controlled; feasibility only | Needed for causal claim, optional for descriptive paper / evaluation lead |
| O5 / optional / 60–90 min | External data or broader chemistry feasibility memo | Current bounded draft stable | Document comparable labels, access, data overlap and new protocol needs before any run | Needed for broad generality, not present paper / data lead |

No expensive refit, sweep, new API collection or laboratory study is approved or required by this plan. The optional tasks above create reviewable protocols/feasibility memos first; actual experiments need a separate scoped decision. Avoid adding a neural framework simply because it appears on a roadmap.

## Minimum credible paper and stopping rules

**Minimum honest first draft:** the fixed source population; exact executed methods; all six branches and all four budgets; conditional within-branch comparisons; explicit post-hoc concentration and optimization diagnostics; verified source citations; a candid availability statement. A system-level superiority claim is absent. E1 supports only a small margin over popularity, alongside much lower coverage than similarity or random selection (file 10). No inferential p-values, discovery claims or assertions that a benchmark proxy measures synthesis success.

**First co-author review stopping rule:** stop expanding scope once (a) Methods v0.1 and Results v0.1 are readable, (b) F1/T1 and the F2/F3 drafts have source links, (c) secondary outcomes are retained, (d) every unresolved result/availability issue is visibly marked, and (e) the contribution comparison and role/decision table are filled enough for review. E1 may be pending at an early review, but comparative system-level language must remain a placeholder. Do not wait for a model win, a new dataset or polished prose to seek review.

**Submission readiness is a later gate:** close every central result placeholder, establish a usable data/analysis availability route, verify literature/attribution, agree author details and contributions, and obtain all co-author approval of the exact manuscript. arXiv is a dissemination route, not a substitute for evidence or a peer-review acceptance claim. No submission is part of this request.

**Scientific stopping rule:** if matched system diagnostics erase the apparent pair advantage, retain that finding and use it to sharpen the evaluation paper. If closest work already makes the same contribution and this dataset adds too little, choose the narrower technical-report/software framing. Do not tune until a favorable result appears.

## Decisions that the repository cannot settle

These are decisions for co-authors, not questions that block this completed planning investigation.

| Decision | Concrete options / proposed default | Who must decide | Record by |
| --- | --- | --- | --- |
| Contribution | Default A: bounded empirical evaluation; B: software paper; C only with new controlled evidence | All prospective authors | C1 |
| Intended endpoint | Default withheld MP provenance recovery; stronger synthesis/chronology endpoint needs new data | Scientific/domain leads | C1 |
| Author list/order and corresponding author | Record actual intellectual contributions and agreements; do not infer from commit counts or metadata | Actual contributors | Before circulation as an authored manuscript |
| Responsibilities | Assign evaluation, domain validation, writing, literature, visualization, reproducibility and data-steward roles; people may hold multiple roles | Each person accepts their tasks | C1 |
| Target audience/venue | Default short materials-informatics empirical report; decide whether arXiv precedes journal submission; verify venue/category later | Authors/corresponding-author role | Q1 |
| Figure selection | Default F1–F3 + T1/T2; architecture sketch only if it resolves a Methods confusion | Writing + domain + visualization leads | C2 |
| Artifact access | What may be shared, under which attribution, and what can an independent reviewer obtain? | Data steward + project owner | D1/R1 |
| Additional experiments | Only if a specific unsupported claim is essential; otherwise narrow the claim | Scientific leads | After first review |
| Feedback mode | Default one structural pass, one evidence pass, one prose pass; annotate claims with C/R IDs | All authors | C1 |
| Affiliations/funding/conflicts | Supply verified details; repository does not establish them | Each author | Before submission |

Feedback checkpoints: C1 decides scope and owners; C2 reviews the first full argument and figures; R1 audits reproduction; final authors review the exact manuscript and availability statement before any release. Consolidate rejected paragraphs, titles and proposed experiments in the parking lot with a reason and a re-entry criterion.
