# Eka Materials Selection: MVP Task Details

Prepared 11 October 2026; updated 13 October 2026. Owner for all tasks: Joshua
Corbett, with Codex assisting. [AGENTS.md](../AGENTS.md) is the authoritative local
board for task status, dependencies, and agent handoffs. This file holds each
task's scope, artifact target, completion criteria, and eventual evidence.

Joshua chose repository-local tracking instead of Linear. There is no pending
publication or browser-access prerequisite. No Linear project or issues were
created. Artifact targets below are proposed paths, not completed deliverables.

The charter and decision log are prepared; the research checkpoint is committed
and the product branch exists. Deferred pilot/reviewer/budget tasks are not blockers.

Add dated evidence, real artifact links, verification results, and limitations to the
relevant section before marking its task Done in AGENTS.md. Keep statuses and
dependencies only in that board to avoid divergent copies.

## MVP-01: Define three demonstration briefs

Create self-authored examples that exercise different tradeoffs. Include an
underspecified brief and an intentionally unsatisfied constraint. Do not present
them as customer cases or validated engineering answers.

Artifact target: `docs/materials-selection-demo-briefs.md`.

Done when: three briefs state supplied facts, unresolved questions, intended
comparison behavior, and what evidence would be needed. Choose exact applications
with MVP-02; the bracket/enclosure/insulator ideas are suggestions, not fixed scope.

Completion evidence, 2026-10-13: [three demonstration briefs](materials-selection-demo-briefs.md)
cover a bracket, an underspecified cover, and a no-supported-match heat-spreader
screen. Each separates supplied inputs, questions, evidence needs, and acceptance
cases. Local links, all 14 task dependencies, three brief IDs, whitespace, and
release audit passed. These are self-authored cases, not executed demos or customer
validation; end-to-end checks remain MVP-11.

## MVP-02: Inventory permitted sources and sample grade coverage

Find manufacturer documentation sufficient for the examples. Record access,
intended use, dates, grade identities, available properties/conditions, and gaps.
Start with sources that can be used without a new paid agreement.

Artifact target: `docs/materials-selection-sources.md`; permitted private source
files, if needed, under `data/local/materials-selection/`.

Done when: each demo has a credible evidence route or an explicitly revised
scope. Manually inspect representative records before choosing a catalogue size.
Do not represent generic family pages as exact commercial grade evidence.

Completion evidence, 2026-10-13: [source inventory](materials-selection-sources.md)
records four inspected grade/alloy references, revision dates, property context,
access failures, sourcing gaps, and manufacturer terms. An additional ceramic
lead is explicitly excluded. No real source is approved for commercial reuse;
the immediate scope is revised to synthetic fixtures while permissions and visual
table checks remain prerequisites for real-data admission in MVP-04. Inventory
links and repository release audit passed; no paid access or outreach occurred.

## MVP-03: Establish the service and material evidence schema

Confirm a small implementation stack and isolate it from the Julia research
package. Model family, grade, variant, property observation, source, task, and
offer identities. Preserve units, conditions, evidence type, and missing values.

Artifact target: `services/materials-selection/` and its schema documentation.

Done when: synthetic examples round-trip through validated storage; distinct
grades stay distinct; provenance survives normalization; dependencies are pinned.
Record the stack decision and checks in the decision log.

Completion evidence, 2026-10-13: [service README and schema](../services/materials-selection/README.md),
[validated models](../services/materials-selection/eka_materials/models.py),
[snapshot storage](../services/materials-selection/eka_materials/storage.py), and
[29 focused tests](../services/materials-selection/tests/test_evidence.py).
Python 3.14.6, Pydantic 2.14.1, Pint 0.26.1, and the standard-library SQLite client
were tested in an isolated environment; all nine runtime packages are pinned.

Checks: 29 service tests and 41 existing Python tests passed; dependency check,
CLI validation/snapshot commands, release audit, and whitespace checks passed.
Tests cover grade separation, dimensional conversions, original provenance,
missing/conflicting values, malformed records, reference integrity, permission
checks, immutable revisions, and read-only retrieval. The synthetic catalogue
round-trip hash is `3b57f1e53e7889f7376a3670c499bb632ad7b0c02e12d56b2511241c79d64c70`.

Limits: only synthetic fixtures are included. This is storage and validation,
not application approval or a comparison engine. Categorical constraints, source
ingestion, UI, model calls, and MCP are not implemented. Julia code was unchanged;
its test suite was not rerun in this session. See decision D10.

## MVP-04: Populate a small traceable catalogue

Ingest and manually check enough grades for the demos. Start from the four
inspected reference candidates; expand only when a demo needs more coverage.
Preserve conflicting observations and revisions; keep source context available.
Use synthetic fixtures for public tests and only permitted real data in the demo.

Artifact target: versioned catalogue under `data/local/materials-selection/` plus
ingestion code and a coverage manifest in the service.

Done when: every decisive value in the demos has exact source evidence, units,
conditions, and a grade identity; repeat ingestion is reproducible.

Handoff, 2026-10-13: begin with the four reference candidates in the
[source inventory](materials-selection-sources.md), not a fixed 15-30-grade quota.
Resolve an adequate rights basis and visually verify source context before
admission. No real records are currently approved or ingested. This gap does not
block MVP-05's synthetic implementation, but it does block real recommendations.

## MVP-05: Implement constraint checks and tradeoff comparison

Implement deterministic pass/fail/unknown/conflict checks and explicit preference
comparisons. Validate observation applicability before numerical comparison.
Keep supported matches and provisional alternatives distinct.

Artifact target: service constraint/ranking functions and focused tests.

Done when: equivalent units agree, unknown never becomes pass, hard failures
cannot be offset by preferences, and supported alternatives expose their tradeoffs.
Check typical-versus-guaranteed values and no-match behavior.

Progress, 2026-11-24: the [material-index worksheet](../services/materials-selection/README.md#compare-a-shortlist-on-a-material-index)
compares manually screened candidates using one explicitly derived power-product
index. The [fictional example](../services/materials-selection/examples/synthetic-index.json)
includes overlapping ranges and an unresolved screen. All 38 service tests
passed, including [nine index checks](../services/materials-selection/tests/test_index_comparison.py).
The CLI example ranked two candidates above a third and withheld the unresolved
candidate. Automatic hard checks on catalogue observations and comparisons
across preferences remain open.

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

## Tracking decision

On 12 October 2026, Joshua replaced the planned Linear setup with a local
AGENTS.md task board. See [decision D07](materials-selection-decisions.md#d07-maintain-a-small-task-board).
External tracker setup is not part of the build sequence. Update, 2026-10-13:
MVP-01 through MVP-03 are complete; the current next-work handoff is in AGENTS.md.
