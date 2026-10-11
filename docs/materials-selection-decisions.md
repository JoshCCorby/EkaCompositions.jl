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

Authorized; local draft prepared; Dialext destination confirmed, 11 October 2026. Codex
prepares the board and decision log. Use 14 MVP issues with owner, dependencies,
artifact, and completion criteria instead of transferring all 118 old tasks.

Access investigation: no Linear connector is exposed in this chat and the in-app
browser is signed out. The Chrome extension connection failed, but desktop control
found an authenticated session in the Dialext workspace with a Dialext team.
Workspace/team confirmation was requested. The attempt to search for existing Eka
records was interrupted when the user changed browser tabs; no issues were
submitted. Resume duplicate checks after the destination is known and browser
control is available. The local backlog is ready but is not a created Linear board.

Follow-up: Joshua instructed Codex to proceed with the proposed Dialext workspace
and team. Desktop browser activity then interrupted both navigation and opening
a separate window. An independent in-app Linear sign-in page is ready; publication
awaits sign-in there or an uninterrupted desktop session. This is an access
blocker, not an outstanding request for permission to create the board.

## D08. Spend and validate in proportion to the stage

Accepted direction, 11 October 2026. Defer the formal pilot budget and named
reviewer. Default to local development and permitted accessible sources; measure
actual model cost. No paid contract, hosting subscription, or reviewer engagement
has been approved.

Still part of the MVP: correct source context, conversions, grade identity,
missing-data behavior, and evidence-backed explanations. Independent application
validation, commercial claims, and commitments require later evidence. Revisit
when the working product reaches an engineer or a specific expense is necessary.
