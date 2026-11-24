# Materials Selection: Decision Log

Started 11 October 2026. Owner: Joshua Corbett. Basis: Joshua's clarification of
P0.1-P0.6 in the project conversation. Accepted directions, implementation
proposals, and hypotheses are distinguished. Update entries with new evidence
without silently replacing their history.

## D01. Build an MVP before a pilot

Accepted, 11 October 2026. Joshua is the sole builder, assisted by Codex. Build
something usable to approach one engineer; do not require a funded pilot,
recruitment programme, or hired specialist first. Replace the earlier dependency
chain and withdraw its schedule. Revisit when a working demo or a concrete
data-access cost creates a need for external participation or funding.

## D02. Support existing-material selection

Accepted, 11 October 2026. Serve engineers in smaller firms/consultancies and
potentially larger firms with materials specialists. Provide a quick reference
with multiple options and tradeoffs; the engineer makes the final design decision.

Hypotheses: many target tasks can use existing materials, and engineering agents
will benefit from reliable selection tools. These are not measured market facts.
Revisit after the first engineer tries a real task. No claim about generative
materials research being restricted to particular industries is needed.

## D03. Keep a broad ambition and declare actual coverage

Accepted direction, 11 October 2026. Broad known-material search is the long-term
ambition. A ceramics-only application and UK/EU market were earlier suggestions,
not user decisions; both defaults are withdrawn.

Implementation proposal: three illustrative briefs and roughly 15-30 documented
grades, across more than one family where feasible. The counts are provisional.
No results means no supported match in the searched sources, not no possible
material. Revisit scope after source inspection and the first complete comparison.

## D04. Evidence and tradeoffs are the core output

Accepted, 11 October 2026. Show pros, cons, relevant conditions, citations,
sourcing links, and unanswered questions. Distinguish documented grade properties,
inference, and missing information. Preferences cannot cancel mandatory failures.
Verify initial source values without making external sign-off a build dependency.
Revisit comparison rules when source context or engineer feedback reveals a flaw.

## D05. Leave the product form open

Accepted direction; delivery details proposed, 11 October 2026. Keep reusable
selection functions for both an interface and other agents. MCP remains intended.
A compact local comparison view is a proposed demonstration surface. A separate
typed service with a small database and official SDK is a stack proposal to
confirm during implementation. Neither multiple agents nor a specific model
provider is a requirement. Revisit with implementation evidence and first-user use.

## D06. Preserve research and branch product work

Completed, 11 October 2026. Saved the 30 pending source, test, paper, and
documentation files in checkpoint commit `2ea4459` on `main`; created
`codex/materials-selection-mvp` from it. The original 8 October plan remains in
that commit. No remote push or publication was performed.

Verification completed: 4,874 Julia checks and 41 Python tests passed. The
repository release audit and whitespace checks passed. This verifies the existing
software checkpoint, not the scientific claims in the paper or a selection MVP.

Existing protocols and score meanings remain as documented. Selection requires
its own evidence; research scores are not measures of application suitability.

## D07. Maintain a small task board

Accepted, 11 October 2026. Codex prepares the board and decision log. Use 14 MVP
tasks with owner, dependencies, artifact, and completion criteria instead of
transferring all 118 old tasks. Joshua initially approved Linear in the Dialext
workspace/team. Access attempts failed; no Linear project or issues were created.

Superseding decision, 12 October 2026: Joshua explicitly requested an AGENTS.md
file instead of Linear. [AGENTS.md](../AGENTS.md) now holds the authoritative
task-status and dependency board; the [backlog](materials-selection-backlog.md)
holds detailed specifications and completion evidence. The charter and this log
remain linked local documents. External publication is no longer planned, and
browser access or security-setting changes are not prerequisites. P0.5 is complete;
the 14 implementation/learning tasks remain open.

Evidence: Joshua's instruction to keep the work in an agents file. Revisit only
if Joshua requests an external tracker or local tracking causes a demonstrated
coordination problem. Keep statuses in one place and require dated artifact and
verification evidence before marking a task complete.

## D08. Spend and validate in proportion to the stage

Accepted direction, 11 October 2026. Defer the formal pilot budget and named
reviewer. Default to local development and permitted accessible sources; measure
actual model cost. No paid contract, hosting subscription, or reviewer engagement
has been approved.

Still part of the MVP: correct source context, conversions, grade identity,
missing-data behavior, and evidence-backed explanations. Independent application
validation, commercial claims, and commitments require later evidence. Revisit
when the working product reaches an engineer or a specific expense is necessary.

## D09. Begin with three cases and a synthetic software fixture

Implementation decision, 13 October 2026. The [demonstration briefs](materials-selection-demo-briefs.md)
cover a bolted bracket, an underspecified hot cover, and a no-supported-match
heat-spreader screen. The [inventory](materials-selection-sources.md) records
four inspected manufacturer references across metals and polymers, plus an
excluded ceramic lead. Replace the provisional 15-30-grade starting estimate
with these four reference candidates; expansion needs an actual comparison need.

Evidence: the inspected documents require temper, thickness, evidence-basis, and
condition distinctions. Published reuse terms do not establish permission to
populate a commercial catalogue. Build and test with fictional grades and values;
do not silently relabel manufacturer values as synthetic or claim the resulting
software selects real materials yet. MVP-02 completes the inventory, not licence
clearance or data ingestion. Real-data admission remains work for MVP-04.

Revisit when one source has an adequate use basis and verified observations, or
when the first comparison exposes a missing material class. No commercial data
contract, source outreach, or legal determination is authorized by this decision.

## D10. Use a small independent Python evidence service

Implemented and tested, 13 October 2026. Use Python 3.14.6 for this initial
environment, Pydantic 2.14.1 for strict typed records/JSON Schema, Pint 0.26.1 for
dimensional checks, and standard-library SQLite for immutable catalogue snapshots.
All runtime packages are pinned in the [service](../services/materials-selection/README.md).
No Julia bridge, web framework, LLM provider, or MCP SDK has been selected or added.

Evidence: 29 focused tests pass, including serialization/storage round trips,
identity/reference checks, original units and provenance, unknowns, conflicts,
permission denials, corruption detection, and temperature/unit conversions. The
41 existing Python tests and repository release audit also pass. CLI validation
and persistence work with the authored synthetic fixture. Julia was unchanged
and its suite was not rerun.

Use separate IDs for families, grades, variants, observations, sources, tasks,
and offers. Keep original bounds and units, with normalized values derived only
when requested. Missing conditions and permissions do not acquire defaults that
claim evidence or authorization. Retention/display decisions are enforced by
storage/CLI, but the stated permission basis remains an importer responsibility.

Store canonical JSON snapshots before adding query indexes: this is sufficient
to verify the evidence model without designing the eventual search backend.
Revisit with the first admitted catalogue's size/query needs or an actual host
integration. Strict/open numeric bounds and categorical requirements need explicit
schema work before use; no silent approximations. Schema validation does not
evaluate constraints or validate an engineer's design.

## D11. Compare manually screened records on one derived index

Implemented 24 November 2026 for a coursework use case. A local worksheet can
identify the material at the level used in the source. It records the user's
screening decision, derivation, and property evidence. Educational material
families can then be compared without inventing commercial grades. Worksheets
are read on demand and do not add records to the evidence catalogue.

The [worked example](../services/materials-selection/examples/synthetic-index.json)
shows two overlapping index ranges and a third that is strictly separated.
Report these pairwise relationships. Revisit the supported mathematical form
when an actual derivation requires additional terms. Revisit integration when
the catalogue can supply checked screening outcomes and applicable observations.
