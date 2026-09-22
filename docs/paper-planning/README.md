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

Drafting order is Methods → Results → Introduction → Discussion → Abstract; the manuscript file uses conventional reading order. Proposed responsibilities remain unassigned. No application code, existing draft, protocol, historical evidence or Git history was edited. No data were queried from MP and nothing was published.

**Update, 22 September 2026 (E0/E1):** the matched system-level comparison is complete. It adds two analysis scripts (`scripts/analyze_matched_system_metrics.py` and `scripts/matched_system_metrics.jl`) and files 09–10. Only saved rankings were re-read; no refit, MP query, application-code change or publication took place.

## What is credible now

The saved experiments demonstrate that the ordering and apparent benefit of four simple ranking methods depend on label policy and holdout design in one fixed source snapshot. Pair-model composition hits can be concentrated in a small number of chemical systems, and aggregate recovery can remain similar while individual top-100 recommendations change with the optimization cap. The software makes those comparisons inspectable.

The like-for-like system-level comparison (E1, file 10) finds the following. In system holdout at K=100, the pair model reaches slightly more positive systems than popularity under all three policies, meeting the pre-stated rule. But both system-level scorers reach one-sixth to one-third as many positive systems as uniform random selection, and at most about half as many as similarity. So composition hits and system coverage order the methods differently. The alternative-policy margins are within cutoff-tie sensitivity. Public exact reproduction and a sharper comparison with closely related literature remain the readiness gaps. These gaps do not prevent an honest first draft with explicit placeholders.

## Next three tasks

E0/E1 are done (files 09–10).

1. Build the complete paired-effect figure and denominator table, retaining all policies and budgets (90–120 minutes each; E2/E3).
2. Draft F2 from the E1 tables, showing composition hits against positive hit systems for all four methods with the random expectation (60–90 minutes; F2).
3. Read the closest literature in full and write a one-page contribution comparison, then hold the first framing review. Bring the C15 metric-divergence finding to that review, since it strengthens framing A (60–120 minutes; L1/C1).
