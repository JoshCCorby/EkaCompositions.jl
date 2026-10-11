# Eka Materials Selection: MVP Task Board

Prepared 11 October 2026. Owner for all issues: Joshua Corbett, with Codex assisting.
Project title for Linear: **Eka Materials Selection MVP**. These are local IDs and
issue drafts; no Linear project or issues have been created yet. Joshua confirmed
the Dialext workspace/team by instructing Codex to proceed. Publication is pending
an uninterrupted desktop session or sign-in through the independent in-app browser.

When publishing, search for existing Eka work first. Reuse an appropriate project
and update matching issues rather than creating duplicates. Resolve Joshua's
actual account and the team's workflow states. Carry dependencies into issue
relations and add artifact links only when those artifacts exist. Record returned
Linear IDs and URLs here after verifying creation.

The charter and decision log are prepared; existing local work is committed and
the product branch exists. Deferred pilot/reviewer/budget tasks are not blockers.

## Overview

| Local ID | Issue | Stage | Status | Dependencies |
| --- | --- | --- | --- | --- |
| MVP-01 | Define three demonstration briefs | Demonstration | Ready | None |
| MVP-02 | Inventory permitted sources and sample grade coverage | Demonstration | Ready | None; coordinate with MVP-01 |
| MVP-03 | Establish the service and material evidence schema | Catalogue | Backlog | MVP-01, MVP-02 |
| MVP-04 | Populate a small traceable catalogue | Catalogue | Backlog | MVP-03 |
| MVP-05 | Implement constraint checks and tradeoff comparison | Selection | Backlog | MVP-03; synthetic data can precede MVP-04 |
| MVP-06 | Attach exact grade sourcing links | Selection | Backlog | MVP-04 |
| MVP-07 | Translate briefs into editable requirements | Agent workflow | Backlog | MVP-01, MVP-03 |
| MVP-08 | Produce evidence-backed shortlist reports | Agent workflow | Backlog | MVP-04, MVP-05, MVP-06, MVP-07 |
| MVP-09 | Build the local comparison interface | Delivery | Backlog | MVP-08 |
| MVP-10 | Expose core operations through MCP | Delivery | Backlog | MVP-05, MVP-06, MVP-07 |
| MVP-11 | Verify the complete demonstration workflow | First-user readiness | Backlog | MVP-08, MVP-09, MVP-10 |
| MVP-12 | Package a runnable first-user demo | First-user readiness | Backlog | MVP-11 |
| MVP-13 | Observe one engineer using a real task | First-user learning | Backlog | MVP-12 |
| MVP-14 | Turn first-user feedback into the next iteration | First-user learning | Backlog | MVP-13 |

## MVP-01: Define three demonstration briefs

Create self-authored examples that exercise different tradeoffs. Include an
underspecified brief and an intentionally unsatisfied constraint. Do not present
them as customer cases or validated engineering answers.

Artifact target: `docs/materials-selection-demo-briefs.md`.

Done when: three briefs state supplied facts, unresolved questions, intended
comparison behavior, and what evidence would be needed. Choose exact applications
with MVP-02; the bracket/enclosure/insulator ideas are suggestions, not fixed scope.

## MVP-02: Inventory permitted sources and sample grade coverage

Find manufacturer documentation sufficient for the examples. Record access,
intended use, dates, grade identities, available properties/conditions, and gaps.
Start with sources that can be used without a new paid agreement.

Artifact target: `docs/materials-selection-sources.md`; permitted private source
files, if needed, under `data/local/materials-selection/`.

Done when: each demo has a credible evidence route or an explicitly revised
scope. Manually inspect representative records before choosing a catalogue size.
Do not represent generic family pages as exact commercial grade evidence.

## MVP-03: Establish the service and material evidence schema

Confirm a small implementation stack and isolate it from the Julia research
package. Model family, grade, variant, property observation, source, task, and
offer identities. Preserve units, conditions, evidence type, and missing values.

Artifact target: `services/materials-selection/` and its schema documentation.

Done when: synthetic examples round-trip through validated storage; distinct
grades stay distinct; provenance survives normalization; dependencies are pinned.
Record the stack decision and checks in the decision log.

## MVP-04: Populate a small traceable catalogue

Ingest and manually check enough grades for the demos, provisionally 15-30.
Preserve conflicting observations and revisions; keep source context available.
Use synthetic fixtures for public tests and only permitted real data in the demo.

Artifact target: versioned catalogue under `data/local/materials-selection/` plus
ingestion code and a coverage manifest in the service.

Done when: every decisive value in the demos has exact source evidence, units,
conditions, and a grade identity; repeat ingestion is reproducible.

## MVP-05: Implement constraint checks and tradeoff comparison

Implement deterministic pass/fail/unknown/conflict checks and explicit preference
comparisons. Validate observation applicability before numerical comparison.
Keep supported matches and provisional alternatives distinct.

Artifact target: service constraint/ranking functions and focused tests.

Done when: equivalent units agree, unknown never becomes pass, hard failures
cannot be offset by preferences, and supported alternatives expose their tradeoffs.
Check typical-versus-guaranteed values and no-match behavior.

## MVP-06: Attach exact grade sourcing links

Map grades or variants to manufacturer/distributor product pages. Capture known
form, geography, date, quantity basis, and availability without inventing offers.

Artifact target: service sourcing records and lookup function.

Done when: every demo candidate has an exact sourcing route or an explicit gap.
Generic family pages are labelled; unverified price/stock/volume capacity remain
unknown. This issue does not authorize contacting suppliers or placing orders.

## MVP-07: Translate briefs into editable requirements

Extract supplied requirements, preferences, assumptions, and open questions into
the task schema. Ask high-value clarifications and let the engineer correct them.
Keep any numerical derivations explicit; vague adjectives are not numeric limits.

Artifact target: service requirements adapter and versioned demo prompts.

Done when: all three briefs produce inspectable specifications with field origins,
and user corrections reach the comparison engine. Malformed model output and
unsupported inferences are rejected or exposed.

## MVP-08: Produce evidence-backed shortlist reports

Combine requirements, comparisons, and sourcing into a report showing advantages,
disadvantages, evidence, assumptions, missing facts, and actual search coverage.

Artifact target: service report function and Markdown/JSON exports.

Done when: three to five options appear when supported, fewer when justified,
every decisive numerical claim cites a matching observation, and insufficient
evidence is an explicit result. Record catalogue and task versions.

## MVP-09: Build the local comparison interface

Create a brief input, editable requirements, comparison table, and source detail
view. Let users change assumptions, compare again, and export the result.

Artifact target: local application in the service and setup instructions.

Done when: the entire workflow works without editing files; values/conditions and
evidence are inspectable; loading, error, empty, and narrow-screen states work.
The first screen is the usable tool. The design does not fix the final product form.

## MVP-10: Expose core operations through MCP

Use an official SDK with a tested release for local stdio tools: validate a
specification, search, inspect grades, compare, and retrieve evidence/sourcing.
Use the same core logic as the interface, with typed inputs/outputs and limits.

Artifact target: service MCP adapter, configuration example, integration checks.

Done when: one real MCP host completes a demonstration and matches the core's
decisions; invalid inputs, timeouts, cancellation, and absent evidence remain
explicit. A host-supplied specification does not require a duplicate model call.

## MVP-11: Verify the complete demonstration workflow

Exercise realistic failures involving units, grade identity, conditions, source
conflicts, unsupported explanation claims, incomplete requirements, and no match.
Treat source-embedded instructions as untrusted content. Verify UI and MCP paths.

Artifact target: focused regression suite and a local demo verification report.

Done when: the three demo briefs complete end to end, decisive claims trace to
sources, known gaps are visible, and cost/latency/manual work are recorded. Results
are labelled software verification, not independent engineering validation.

## MVP-12: Package a runnable first-user demo

Prepare a stable local build with clear setup, example briefs, synthetic fixtures,
and instructions for acquiring/loading any permitted private catalogue inputs.

Artifact target: service README, reproducible dependency setup, demo bundle.

Done when: setup works from a clean environment; an engineer can inspect a result,
change a requirement, and compare again; restricted data and credentials are
excluded from public packaging. Public hosting is optional.

## MVP-13: Observe one engineer using a real task

Joshua approaches an engineer with the working MVP. Observe a task and record
useful suggestions, disputed comparisons, missing information, and usability
friction. Get permission before retaining private project information.

Artifact target: private first-user notes and a de-identified findings summary.

Done when: one engineer tries a real task and provides concrete observations.
Do not count a demonstration or interest alone as validated accuracy or demand.
This task is future owner outreach, not a message sent by this planning turn.

## MVP-14: Turn first-user feedback into the next iteration

Prioritize observed failures and useful improvements. Reconsider the initial
application, sources, interface, and whether specialist review or a formal pilot
now answers a concrete need. Re-estimate using actual implementation experience.

Artifact target: updated backlog and dated decision-log entries.

Done when: the next small iteration is justified by observed use, with clear
completion criteria; deferred work stays deferred unless evidence warrants it.

## Linear publication record

- Workspace/team: Dialext, confirmed by Joshua's instruction to proceed.
- Project URL: not created.
- Issue mappings: none created.
- Existing work to check for duplication: Eka projects and materials-selection issues.
- Access: no connector exposed. Desktop actions were interrupted by browser
  activity, including an attempt to open a separate window. Linear's sign-in
  page is open in the independent in-app browser. No issues were submitted.
- Local planning artifacts: this board, the charter, plan, and decision log.
