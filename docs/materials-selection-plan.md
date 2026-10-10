# Eka Materials Selection: MVP to First User

Revised 11 October 2026 following Joshua's clarification. This replaces the
8 October pilot-first sequence, retained in Git at `2ea4459`. Its recruitment,
reviewer, budget, and benchmark targets are not current prerequisites. Product
implementation has not started.

## Direction

Build a quick, inspectable materials reference for engineering firms,
consultants, and materials specialists. An engineer describes a design problem;
Eka proposes existing materials, explains their pros and cons, and links to the
evidence and sourcing options. Other engineering agents can use the same service.

Joshua is the sole builder. The immediate objective is a working MVP to show a
potential first user. Engineer feedback will help determine the final product
form. A funded pilot, hired reviewer, interviews, and a fixed industry niche are
not entry requirements.

The long-term ambition is broad search across known materials. The MVP will
disclose the sources and material classes actually searched. A limited catalogue
cannot support a claim of searching every known material, and an empty result
cannot establish that no suitable material exists.

- [One-page charter](materials-selection-charter.md)
- [Decision log](materials-selection-decisions.md)
- [Task board and Linear issue drafts](materials-selection-backlog.md)

## Phase 0 decisions

| Original item | Current disposition | Evidence or next action |
| --- | --- | --- |
| P0.1 Charter | Done | Charter records the user's direction and open product decisions |
| P0.2 Pilot budget | Deferred | Track MVP costs; consider paid data/hosting when a specific need appears |
| P0.3 Named technical reviewer | Deferred | Joshua builds the prototype; first engineer feedback precedes a formal review programme |
| P0.4 Commit and branch | Done | Existing work saved in `2ea4459`; branch is `codex/materials-selection-mvp` |
| P0.5 Task board | Local draft ready; Linear destination pending | Backlog has owners, dependencies, artifacts, and completion criteria; the identified workspace is Dialext |
| P0.6 Decision log | Done | Accepted decisions, proposals, and hypotheses are recorded separately |

## Build sequence

| Stage | Result | Issue IDs |
| --- | --- | --- |
| 1. Define a small demonstration | Three example briefs and a usable source set | MVP-01, MVP-02 |
| 2. Establish the evidence model | Distinct grades, comparable properties, exact citations | MVP-03, MVP-04 |
| 3. Make comparisons work | Constraint checks, tradeoffs, and sourcing links | MVP-05, MVP-06 |
| 4. Add the agent workflow | Brief interpretation and evidence-backed reports | MVP-07, MVP-08 |
| 5. Make it usable | Small comparison interface and MCP access | MVP-09, MVP-10 |
| 6. Prepare a first-user demo | Reliability checks and reproducible setup | MVP-11, MVP-12 |
| 7. Learn from an engineer | One observed real task and prioritized corrections | MVP-13, MVP-14 |

These are local planning identifiers, not Linear issue IDs. Joshua owns all work;
Codex can assist with implementation and board maintenance. Completion criteria
and artifact targets are in the backlog. Implementation starts after this planning
revision; this document does not claim a working product already exists.

## 1. Define a small demonstration

Write three illustrative engineering briefs. They can be self-authored and must
be labelled as demonstrations, not customer research or an engineering benchmark.
Choose them against available evidence so they are feasible to implement.

Possible examples are a lightweight bracket, a temperature-exposed enclosure,
and an electrically insulating component that must transfer heat. These are
proposals, not commitments to particular applications or materials. Include
incomplete requirements and competing priorities.

Keep the input model general. If practical, cover more than one material family;
do not force breadth when reliable comparisons are missing. A seed set of roughly
15-30 commercial grades is an estimate, not a quota.

Build a source register: manufacturer, document URL, grade coverage, revision and
access date, acquisition method, storage/display permissions, and gaps. Use
accessible, permitted sources initially. Public visibility does not establish
republication rights. Synthetic records can unblock implementation while real
data access is unresolved.

Done when: three briefs and a small source set support an end-to-end demo. No
recruited engineer is needed to start.

## 2. Establish the evidence model

Use separate identifiers for material families, manufacturer grades, product
forms, observations, sources, and supplier listings. Composition is optional
metadata; it does not uniquely identify a commercial grade.

Each observation needs its value/range, units, applicable conditions, test method
where stated, typical versus specified-limit status, evidence type, source
revision, and exact page/table or other location. Preserve missing facts and
conflicting observations. Do not merge different grades or conditions.

Manually check the initial decisive observations. Automated extraction can propose
entries, but ambiguous headers, units, and footnotes need resolution before the
values qualify a candidate. Publish a versioned catalogue.

Keep the Julia research package and frozen protocols intact. The proposed new
service lives under `services/materials-selection/`, with typed data, SQLite, a
tested units library, and a thin MCP adapter. Python remains a proposal to confirm
in a small implementation spike. Do not introduce a Julia/Python runtime bridge
unless a specific reusable capability justifies it.

Done when: each decisive demo value resolves to a grade, condition, and source;
unchanged inputs reproduce the catalogue identity.

## 3. Make comparisons work

Implement grade/alias lookup and structured property filters first. Evaluate hard
requirements before preferences. Each constraint returns pass, fail, unknown, or
conflicting evidence with the observations and rule used.

Check units, temperature, processing state, direction, and evidence requirements
before comparing values. A typical value cannot establish a guaranteed minimum.
Unsupported extrapolation and missing conditions remain unknown.

Show alternatives and the reasons to choose or reject them. Expose where improving
one preference sacrifices another. Use visible weights only when useful; never
let a preference score cancel a failed hard constraint. Separate provisional
candidates from supported matches.

Link exact grades/products to manufacturers or suppliers. Show quantity, region,
price basis, availability, and date only when documented. A product page supports
a sourcing route; it does not prove stock or volume capacity. Accept geographic
preferences without imposing UK/EU as the product's market. Supplier outreach,
quotations, and purchasing remain outside this MVP.

Done when: structured requests produce reproducible comparisons and sourcing
links or explicit sourcing gaps without an LLM.

## 4. Add the agent workflow

Translate a brief into function, environment, geometry, manufacturing, supplied
limits, preferences, and unknowns. Separate user statements from model suggestions
and derived requirements. Ask questions likely to change the comparison.

Initially collect and clarify engineering limits rather than inferring detailed
physics from vague descriptions. Add a numerical derivation only when its formula,
inputs, units, and validity assumptions are explicit and tested. Let the engineer
correct the proposed specification.

Have the model call the comparison engine and explain its outputs. The evidence
store supplies values; deterministic rules perform numerical checks. Retrieved
content is data, not instructions. A multi-agent scientist or autonomous research
loop is not necessary for the first version.

Return roughly three to five options when supported, with advantages,
disadvantages, decisive evidence, unknowns, and sourcing links. Return fewer or
an insufficient-evidence result when appropriate. Include coverage and assumptions
that could change the answer.

Done when: a demo brief can be clarified, searched, and explained with every
decisive numerical claim grounded in a returned observation.

## 5. Make it usable

Provide a small local interface: brief, editable requirements, comparison table,
and source detail. Open directly into selection. Export the task, tradeoffs,
sources, and catalogue version. This is a demonstration surface; the eventual
product could become agent-first, browser-first, or both.

Expose the same functions through MCP: validate requirements, search, inspect a
grade, compare, and retrieve evidence/sourcing. Use an official SDK, pin a tested
release, and start with local stdio. A host agent can prepare the specification
without duplicating an internal model call. Handle malformed inputs, absent
data, cancellation, and errors. Hosted access and accounts follow actual demand.

Done when: the interface and an MCP client can produce the same comparison
without manually repairing the data.

## 6. Prepare the first-user demo

Check identity, units, boundaries, wrong conditions, conflicting sources, hard
failures masked by preferences, unknowns treated as passes, broken citations,
and no-match cases. Include out-of-coverage questions and misleading instructions
embedded in a source. These are software checks, not application approval.

Run the three demonstration briefs end to end. Record latency, model cost,
failures, and manual interventions. Check source links and exports. Test setup
from a clean environment with synthetic fixtures. Keep restricted data, private
briefs, and credentials out of Git.

Package a runnable build, short setup instructions, and example tasks. A stable
local demo that an engineer can inspect and challenge is enough; public launch,
a formal benchmark, and multiple recruited firms are not requirements.

Done when: all three demos work, decisive claims are traceable, coverage is
visible, and a first engineer can try the workflow.

## 7. Learn from one engineer

Approach one engineer with the working MVP. Observe a real task and record useful
suggestions, missing facts, disputed comparisons, and usability problems. Get
permission before retaining or transmitting confidential project information.

Prioritize corrections and another real use. Let experience determine initial
applications, coverage, interface, and specialist-review needs. A demonstration
does not establish demand, design qualification, or broad accuracy.

A structured pilot, independent review, held-out evaluation, paid data access,
hosting, and payment tests become relevant afterward when they answer observed
questions. Keep final design decisions with the responsible engineer.

## Deferred work

- Recruiting several firms or hiring a specialist before building.
- A formal pilot budget, payment targets, and a 20-task held-out benchmark.
- Complete database aggregation, exhaustive coverage claims, and broad crawling.
- Generative material design and learned property prediction.
- Automated qualification, supplier contact, and purchasing.
- Enterprise accounts, CAD/FEA integrations, and multi-tenant hosting.

Basic source checks, correct comparisons, and honest unknowns belong in the MVP.
The deferred work is a later product programme, not a condition of beginning.

## Next step

Start with MVP-01 and MVP-02: three demo briefs and enough source evidence to
support them. Build one complete comparison before expanding. Re-estimate after
that first path works. The earlier 12-16 week beta schedule is withdrawn because
it assumed a different team and validation sequence.
