# Eka paper planning

Investigation date: 22 September 2026. Audited Git HEAD: `0629ba9d600afcd0cdbf1ddfc30ef83dbe6088c4` (`v0.1.1`), with pre-existing uncommitted work. This is an editable planning package, not a submission or a claim of publication readiness.

**Recommendation:** develop a short empirical evaluation paper, with Eka as its reproducible software vehicle. The supported subject is recovery of withheld Materials Project experimental-provenance labels in oxygen-containing ternaries. It is not experimental discovery or a new state-of-the-art predictor.

## Read in this order

1. [Repository and research-history map](01-repository-history.md).
2. [Evidence audit and paper direction](02-evidence-and-framing.md).
3. [Annotated IMRaD skeleton and initial prose](03-manuscript-skeleton.md).
4. [Figure and table storyboard](04-figure-storyboard.md).
5. [Small-task backlog and co-author decisions](05-backlog-and-decisions.md).
6. [Parking lot](06-parking-lot.md).
7. [Focused literature record](07-literature.md).
8. [Checks performed for this investigation](08-verification.md).
9. [E0 matched system-metric specification](09-e0-system-metrics-spec.md).
10. [E1 matched system-metric results](10-e1-system-metrics-results.md).
11. [L1 nearest-work comparison and C15 novelty check](11-l1-nearest-work.md).
12. [Writing guide: what to write, where to find it](12-writing-guide.md).

Drafting order is Methods → Results → Introduction → Discussion → Abstract; the manuscript file uses conventional reading order. Proposed responsibilities remain unassigned. No application code, existing draft, protocol, historical evidence or Git history was edited. No data were queried from MP and nothing was published.

**Update, 22 September 2026 (E0/E1):** the matched system-level comparison is complete. It adds two analysis scripts (`scripts/analyze_matched_system_metrics.py` and `scripts/matched_system_metrics.jl`) and files 09–10. Only saved rankings were re-read; no refit, MP query, application-code change or publication took place.

## What is credible now

The saved experiments demonstrate that the ordering and apparent benefit of four simple ranking methods depend on label policy and holdout design in one fixed source snapshot. Pair-model composition hits can be concentrated in a small number of chemical systems, and aggregate recovery can remain similar while individual top-100 recommendations change with the optimization cap. The software makes those comparisons inspectable.

The like-for-like system-level comparison (E1, file 10) finds the following. In system holdout at K=100, the pair model reaches slightly more positive systems than popularity under all three policies, meeting the pre-stated rule. But both system-level scorers reach one-sixth to one-third as many positive systems as uniform random selection, and at most about half as many as similarity. So composition hits and system coverage order the methods differently. The alternative-policy margins are within cutoff-tie sensitivity. Public exact reproduction and a sharper comparison with closely related literature remain the readiness gaps. These gaps do not prevent an honest first draft with explicit placeholders.

## Next three tasks

E0/E1 and L1 are done (files 09–11). L1 finds that C15 applies an established virtual-screening and recommender-systems idea to materials benchmarks; it is not a new metric. Chung et al. 2025 already shows label-scheme dependence, and SynCoTrain uses an MP experimental/theoretical endpoint close to Eka's.

Figures and tables T1, T2, F1, F2, F3, S1 and the label-mode table are built (E2–E4, F2, F3; `reports/local/paper-figures-2026-09-22/`). The author works alone.

1. Confirm framing A and the title, then write Methods v0.1 using [file 12](12-writing-guide.md) (W1).
2. Write Results v0.1 around T1, F1/T2, F2 and F3 (W2).
3. Write the Introduction, Discussion and Abstract (W3–W5). In parallel, close the L1 open items and write the data-availability statement (D1/V1).
