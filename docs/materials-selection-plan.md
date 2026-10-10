# Eka Materials Selection: Delivery Plan

Prepared 8 October 2026. Status: draft for execution; implementation has not
started. Checkboxes describe future work, not completed capabilities.

## 1. Product decision

Build a service that turns an engineering brief into a defensible shortlist of
existing material grades, with property evidence and exact sourcing links. Make
that service available to engineering agents through MCP and to engineers through
a small comparison interface.

The first outcome to prove is: an engineer can reach an acceptable shortlist
faster, with fewer unsupported assumptions, than with their current workflow or
a general AI assistant using web search.

The broad ambition is materials search across many applications. The initial
product is deliberately bounded so its answers can be checked.

### Working assumptions

| Decision | Proposed starting point | When to confirm |
| --- | --- | --- |
| First user | An electronics engineer choosing a ceramic substrate for thermal management and electrical insulation | Phase 1 |
| First buying region | UK/EU; expand when actual pilot users require another region | Phase 1 |
| First task | Compare commercially offered substrate grades for a defined application | Phase 1 |
| First data set | 30-60 distinct manufacturer grades from at least three manufacturers, subject to useful coverage and permitted use | Phase 2 |
| Evaluation set | 20 real tasks: eight development tasks and 12 held-out tasks, plus synthetic failure cases | Phase 3 |
| First users | Three to five engineers, with access to an experienced materials reviewer | Phase 1 |
| Delivery | Local MCP service and a compact comparison view; hosted service after pilot evidence | Phases 8-12 |
| Team | Joshua owns product and implementation; a practicing engineer reviews technical judgments | Phase 0 |

These numbers are planning targets. Record changes and their reasons before
evaluating the final system. A smaller well-supported catalogue is preferable to
padding the count with duplicate listings or poorly documented grades.

### What the first release delivers

- A structured brief separating supplied facts, derived requirements, assumptions,
  hard constraints, preferences, and unresolved questions.
- A shortlist of up to five specific grades, with alternatives where tradeoffs
  matter and explicit reasons when nothing qualifies.
- Property-level citations, units, test conditions, and evidence status.
- Manufacturer, grade, available product form, and supplier or quotation links.
- Clear distinctions between documented properties, product availability, and
  suitability that still needs engineering or supplier validation.
- A saved comparison that can be reproduced against a versioned catalogue.

Defer novel material generation, learned property prediction, broad web crawling,
automatic supplier outreach or purchasing, automated qualification, CAD/FEA
integration, and coverage of all material families. These are later product
decisions, not prerequisites for the pilot.

## 2. Relationship to the current repository

Eka's existing composition rankings and recovery experiments do not measure
application suitability. A reduced chemical formula is not a commercial grade.
The current working tree also contains evaluation and paper work in progress.

- Preserve the existing Julia package, public API, CLI, frozen protocols, and
  scientific evidence. Track their work separately from this product plan.
- Reuse the project's provenance and evaluation practices. Do not reinterpret
  stored composition scores as engineering suitability or production readiness.
- Introduce independent identifiers for material families, manufacturer grades,
  property observations, and supplier offers. Composition is optional metadata.
- Keep real supplier data and customer briefs in appropriately restricted local
  storage initially. Existing repository rules put local data under
  `data/local/` and local results under `reports/local/`; those are not release
  contents. Public fixtures must be synthetic or explicitly cleared.
- Record a separate selection evaluation protocol before final testing. Do not
  amend the existing research protocols to accommodate this task.

See [contribution rules](../CONTRIBUTING.md), [API stability](api-stability.md),
and the [evaluation roadmap](evaluation-roadmap.md) for the existing boundaries.

## 3. Sequence and checkpoints

| Phase | Work | Depends on | Tangible result |
| --- | --- | --- | --- |
| 0 | Define ownership and project boundaries | None | One-page charter and task board |
| 1 | Validate the user and application | 0 | Real briefs and initial pilot participants |
| 2 | Prove data access and manual usefulness | 1 | Reviewed manual recommendations and source register |
| 3 | Specify the evaluation | 1-2 | Frozen pilot protocol and separated tasks |
| 4 | Build the grade and evidence catalogue | 2-3 | Validated, versioned data store |
| 5 | Implement filtering and comparison | 4 | Deterministic selection engine |
| 6 | Add brief interpretation | 3, 5 | Reviewed requirements workflow |
| 7 | Add sourcing and scale evidence | 4-6 | Exact product links and sourcing status |
| 8 | Expose the service through MCP | 5-7 | Working agent integration |
| 9 | Add the engineer's comparison view | 5-7; can overlap 8 | Inspectable and exportable decisions |
| 10 | Run the held-out evaluation | 3-9 | Complete quality and speed report |
| 11 | Run a live pilot and test payment | 10 | Usage, decision outcomes, and commercial evidence |
| 12 | Package, operate, and expand | 11 | Supported beta or an explicit change in direction |

Critical path: useful real tasks -> usable source data -> reviewed manual answers
-> deterministic comparisons -> agent workflow -> independent evaluation -> live
usage. Participant recruitment and supplier data discussions can continue while
software is built. External outreach is a task for the owner; this plan does not
send messages or make commitments.

## Phase 0. Establish the project

Owner: Joshua. Effort allowance: one to two working days.

- [ ] P0.1 Write a one-page charter covering the user, decision, application,
  initial geography, intended output, and explicit exclusions above.
- [ ] P0.2 Choose a pilot budget covering reviewer time, data access, model usage,
  hosting if needed, and contingencies. Obtain actual quotes where costs are
  material; do not assume catalogue access is free.
- [ ] P0.3 Secure a named technical reviewer and define what they review:
  requirement derivation, property comparability, and recommendation validity.
- [ ] P0.4 Account for current uncommitted work before implementation. Use a
  dedicated product branch or managed worktree when needed; preserve research
  work and its ownership. A new checkout must use an intentional base.
- [ ] P0.5 Create a task board using the task IDs in this document, with an owner,
  dependency, artifact link, and completion evidence for each task.
- [ ] P0.6 Start a decision log. Record assumptions, dates, supporting evidence,
  and what observation would change each important decision.

Completion: scope, reviewer, budget ceiling, and ownership are explicit. Do not
make research publication completion an artificial dependency of the pilot.

## Phase 1. Confirm the first engineering problem

Owner: Joshua, with participating engineers. Effort allowance: three to five
working days, plus recruitment and scheduling delays.

- [ ] P1.1 Interview five to eight people who perform material selection. Aim to
  include design engineers, a materials specialist, and a procurement contact.
- [ ] P1.2 Ask each person to walk through a recent decision: application, initial
  information, missing inputs, sources searched, alternatives rejected, time
  spent, final choice, and what happened after selection.
- [ ] P1.3 Establish where the difficulty actually lies: translating requirements,
  comparing datasheets, finding alternatives, checking availability, or getting
  a material qualified. Record the frequency and consequence of that difficulty.
- [ ] P1.4 Obtain permission to retain and evaluate de-identified task briefs.
  Record confidential fields and who may access them. Keep customer information
  out of public fixtures and third-party search queries unless permitted.
- [ ] P1.5 Gather 20 distinct tasks where possible. Historical cases are useful,
  but capture the information available at the time of the original decision.
  Preserve final decisions separately for the evaluator.
- [ ] P1.6 Score possible starting applications for repeated demand, source
  coverage, access to reviewers, sourcing complexity, and willingness to pay.
  Confirm ceramic substrates or record a better-supported choice.
- [ ] P1.7 Recruit three to five pilot engineers and identify the budget owner.
  Agree what they will try and what evidence they will share afterward.
- [ ] P1.8 Describe the full decision boundary: substrate material, geometry,
  metallization, joining, and assembly conditions may interact. Record what the
  pilot can compare and what remains outside its calculation model.

Interview prompts: "Show me your last selection", "Which facts were hardest to
verify?", "What made a candidate unacceptable?", "What did you do after finding
a supplier?", and "Who pays for the tools or engineering time involved?"

Checkpoint A: continue when several engineers describe the same recurring task,
at least three will try the workflow, and usable real briefs exist. If the main
pain is elsewhere, revise the application before building the catalogue.

## Phase 2. Prove the answer manually and secure sources

Owner: Joshua; reviewer checks technical comparisons. Effort allowance: four to
seven working days, plus any data access discussions.

- [ ] P2.1 Inventory candidate sources: manufacturer grade datasheets and
  application guides, distributor product pages, permitted customer data, and
  licensed reference databases where useful.
- [ ] P2.2 Build a source register containing owner, URL, document revision,
  access date, acquisition method, permitted storage/display/redistribution,
  attribution, refresh method, access costs, and unresolved restrictions.
- [ ] P2.3 Verify intended commercial and automated uses for each source. Where
  reuse is unresolved, use an allowed source or keep the proposed integration
  pending. Public visibility alone does not establish reuse permission.
- [ ] P2.4 Extract ten representative grades by hand from at least three
  manufacturers. Include awkward cases: incomplete conditions, conflicting
  revisions, and a distributor name that differs from the manufacturer name.
- [ ] P2.5 Measure coverage for the properties required by the collected tasks.
  Count observations with relevant conditions, not just populated fields.
- [ ] P2.6 Produce three to five manual selection reports on development tasks.
  Include requirement questions, constraint status, alternatives, source evidence,
  exact grade links, and sourcing unknowns.
- [ ] P2.7 Have the engineer and reviewer mark unsupported claims, missing
  constraints, unusable comparisons, and useful outputs. Revise the report format.
- [ ] P2.8 Record how long manual curation and each selection take. Estimate the
  ongoing cost of maintaining the catalogue from measured work.
- [ ] P2.9 Compare this workflow with tools participants already have. Granta
  offers systematic selection and substitution
  ([Granta documentation](https://ansyshelp.ansys.com/public/Views/Secured/Granta/v261/en/Selector/sel_edu/selector.html));
  Total Materia offers multi-criteria ranking
  ([Optimizer documentation](https://www.totalmateria.com/en-us/horizon/optimizer/)).
  Identify the specific improvement users value.

Manufacturer documentation is a plausible starting source:
[CoorsTek lists ceramic material datasheets and electronic substrate guides](https://www.coorstek.com/en/resources/brochures-datasheets/).
This is a source lead, not a statement that its content can be freely republished.

Checkpoint B: at least three manual reports are useful to their intended users,
the reviewer can substantiate their central claims, and a practical data-access
route exists. Otherwise narrow or change the task before automating extraction.

## Phase 3. Define success before tuning

Owner: Joshua and the technical reviewer. Effort allowance: two to four working
days. Complete before inspecting final evaluation outcomes.

- [ ] P3.1 Write `docs/materials-selection-evaluation-protocol.md` with the task
  population, permitted inputs, source snapshot, comparators, review rubric,
  metrics, decision thresholds, failure rules, and versioning policy.
- [ ] P3.2 Split the planned 20 real tasks into eight development and 12 held-out
  tasks. Group variants from the same project or near-identical application into
  one partition. Manual reports from Phase 2 belong to development only.
- [ ] P3.3 Have an evaluator retain held-out desired outcomes and annotations.
  Withhold them from prompt design, ranking design, and curation targeted at
  improving answers. Normal relevant datasheets may remain searchable.
- [ ] P3.4 For each task, define critical clarification questions, non-negotiable
  constraints, acceptable evidence, multiple acceptable grades where appropriate,
  and conditions requiring an insufficient-evidence or no-match response.
- [ ] P3.5 Set three comparators: the engineer's usual workflow; a general AI
  assistant with web search; and the same assistant with Eka's catalogue and
  selection tools. Match time budgets and starting information where possible.
- [ ] P3.6 Keep the model/version comparable for the two assistant conditions.
  Record differences in tools, sources, access, and human assistance explicitly.
- [ ] P3.7 Separate mechanical correctness from engineering usefulness. A valid
  schema or an existing citation does not establish that the evidence supports
  the claim or that the material meets the application.
- [ ] P3.8 Define review procedures before running: hide system identity when
  practical; have a second reviewer check critical failures and a sample of
  remaining decisions; record disagreements and their resolution.
- [ ] P3.9 Add synthetic cases for contradictory requirements, missing units,
  unavailable grades, incompatible conditions, out-of-scope tasks, and no feasible
  candidates. Keep their results separate from real-task results.
- [ ] P3.10 Freeze the protocol and task partition now. Specify how the finished
  catalogue, prompts, and software will be frozen before Phase 10; the catalogue
  is still being built. Tuning after a final run requires a new evaluation
  version and fresh held-out tasks.

### Proposed pilot decision thresholds

These are operational targets to ratify before testing, not measured performance
or a statistical guarantee from a small sample.

| Measure | Definition | Initial continuation target |
| --- | --- | --- |
| Critical false pass | A recommended-as-qualified grade violates a hard constraint or claims qualification without required evidence | Zero in the evaluated tasks |
| Traceability | Decisive property and sourcing claims link to the exact source observation | 100% |
| Claim support | Reviewer judges a decisive claim supported under the stated conditions | 100%; any unsupported decisive claim is a repair item |
| Useful shortlist | At least one of the top three is judged worth the engineer's next validation step | At least 80% of predesignated answerable held-out tasks |
| Appropriate abstention | Correct handling of cases requiring clarification, no-match, or insufficient evidence | All predefined must-abstain cases; also report unnecessary abstentions |
| Time saved | Reduction in median active time to an accepted shortlist relative to usual workflow | At least 30%, without worse decision quality |
| Product advantage | Improvement over the general assistant under the same rubric | A material quality or time advantage, with the tradeoff reported |

Report raw task counts and denominators alongside percentages. Designate
answerable tasks independently before the run; missing answers do not disappear
from the report. Report all-task coverage, completion, errors, and abstentions.
Do not claim broad industry performance from this pilot.

## Phase 4. Build the material and evidence catalogue

Owner: Joshua; reviewer approves curated evidence. Effort allowance: six to nine
working days. Start with the manually checked records from Phase 2.

### Architecture decision

Proposed default: an independently versioned Python service under
`services/materials-selection/`, using SQLite for the initial catalogue, typed
schemas, a tested units library, and the
[official Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk). Keep the
selection logic callable without an LLM or an MCP session. This adds a product
service without changing the Julia research package or introducing a mandatory
Julia/Python runtime bridge.

Confirm this choice in a short architecture record after a small SDK and ingestion
spike. If implementation experience strongly favors another supported stack,
record the change before expanding. Pin a tested SDK release and the negotiated
protocol version; do not build against an unpinned development branch.

Proposed layout, created during implementation:

```text
services/materials-selection/
  pyproject.toml
  src/eka_selection/
    models.py
    catalogue.py
    ingest/
    constraints.py
    ranking.py
    requirements.py
    sourcing.py
    mcp_server.py
  tests/
    fixtures/                 # Synthetic JSON/CSV and document examples
  README.md
data/local/materials-selection/       # Restricted real inputs and catalogue
reports/local/materials-selection/    # Local runs and evaluation outputs
```

Check the repository's release rules before choosing fixture formats: the
existing release audit rejects most database and JSONL files. Store environment
pins for this service in a reviewed format consistent with those rules.

### Minimum data model

| Entity | Required information |
| --- | --- |
| Material family | Stable ID, name, aliases, application taxonomy, optional composition |
| Manufacturer grade | Stable ID, manufacturer, designation, family, grade revision/status, processing or condition where known |
| Product variant | Grade ID, form, dimensions or ranges, surface treatment/metallization, relevant manufacturing conditions |
| Property observation | Subject ID, property, value/range/curve, original and normalized units, temperature, direction, test method, specimen/condition, evidence type, typical/minimum/maximum status |
| Source record | URL or permitted internal locator, title, publisher, revision, access date, checksum where permitted, page/table/row, rights and review status |
| Supplier offer | Exact grade/variant mapping, supplier, product or RFQ URL, geography, quantity basis, currency, price/lead time if documented, verification time |
| Task specification | Brief version, supplied facts, derived requirements and calculations, hard constraints, preferences, assumptions, open questions |
| Selection run | Task/catalogue/engine versions, eligible/excluded/unknown candidates, constraint results, ranking components, citations, timestamps |

- [ ] P4.1 Define schemas and stable IDs. Different manufacturer grades remain
  distinct even when their nominal chemical formula is identical.
- [ ] P4.2 Define property names, unit dimensions, range semantics, applicable
  conditions, and evidence types with the reviewer. Prefer an established units
  library over handwritten conversions.
- [ ] P4.3 Define typical versus guaranteed values and supplier-reported versus
  independently measured versus predicted evidence. A generic confidence score
  must not replace these distinctions.
- [ ] P4.4 Implement source acquisition for permitted sources with bounded retries,
  caching, revision detection, and retrieval timestamps. Prefer structured feeds
  or exports when offered; add document parsing only where needed.
- [ ] P4.5 Build an ingestion pipeline: acquire -> extract -> normalize -> validate
  -> review -> publish a catalogue version. Keep original values and their source
  locations so every transformation can be checked.
- [ ] P4.6 Treat automated/LLM extraction as proposed data until validated.
  Quarantine ambiguous cells, merged headers, footnotes, and mismatched units.
  Extraction uncertainty cannot become a precise engineering observation.
- [ ] P4.7 Add duplicate and alias resolution. Merge duplicate listings only with
  evidence of identity; preserve different grades, conditions, and revisions.
- [ ] P4.8 Preserve conflicting observations rather than averaging them away.
  Record precedence rules, superseded versions, and unresolved conflicts.
- [ ] P4.9 Review all initial decision-critical observations, then expand toward
  30-60 grades. Track source and task coverage, not just total record count.
- [ ] P4.10 Publish immutable catalogue versions with an acquisition manifest and
  a reversible update procedure. Runtime selection reads a known version.
- [ ] P4.11 Verify units, identity, ranges, revision changes, and provenance with
  focused tests using synthetic examples and the manually checked reference set.

Completion: an engineer can follow every decisive catalogue value to its exact
source context, and repeated ingestion of unchanged inputs preserves identity
and meaning. Coverage is sufficient for the agreed application.

## Phase 5. Implement reliable selection and tradeoffs

Owner: Joshua, with reviewer sign-off on comparison rules. Effort allowance:
four to six working days.

- [ ] P5.1 Implement exact grade/alias lookup and structured property filtering.
  Start with database queries and simple text search. Add embeddings only if
  measured retrieval failures justify them.
- [ ] P5.2 Represent every hard-constraint check as pass, fail, unknown, or
  conflicting evidence. Store the observation IDs and comparison rule used.
- [ ] P5.3 Make compatibility checks precede numerical comparisons. Data measured
  at room temperature cannot establish a high-temperature requirement, and a
  differently processed specimen may not represent the offered product.
- [ ] P5.4 Specify how ranges, curves, tolerances, and typical values are used.
  For a guaranteed lower bound, a typical value alone cannot establish a pass.
  Interpolation needs an explicit validated rule; unsupported extrapolation is
  unknown. Label any provisional screening assumptions in the result.
- [ ] P5.5 Enforce hard constraints before preference ranking. A better cost or
  thermal score must never cancel a failed mandatory requirement.
- [ ] P5.6 Display a supported shortlist separately from candidates requiring
  additional evidence. If all candidates have critical unknowns, return that
  outcome rather than silently relaxing the task.
- [ ] P5.7 Compare the feasible candidates on a small set of explicit preferences.
  Show the non-dominated options: candidates for which improving one objective
  requires sacrificing another. Add a weighted order only with visible weights
  and meaningful, fixed normalization scales.
- [ ] P5.8 Explain score components and test sensitivity to reasonable preference
  changes. Missing preference data must not receive a favorable invented value.
  Never label a ranking score as a probability of engineering success.
- [ ] P5.9 Use stable tie-breaking and record the exact candidate set. Return
  exclusion reasons, catalogue coverage, and unresolved evidence alongside hits.
- [ ] P5.10 Test boundary values, equivalent units, absent data, incompatible
  conditions, conflicting observations, preference reversals, and no-match cases.
  Review representative outputs without involving an LLM.

Completion: the same structured request and catalogue produce the same selection,
and an independent reviewer can reconstruct every qualification and tradeoff.

## Phase 6. Translate briefs into engineering requirements

Owner: Joshua and the technical reviewer. Effort allowance: four to six working
days, using development tasks only.

- [ ] P6.1 Create a brief schema for function, environment, continuous/peak
  temperature, electrical isolation, heat flow, geometry, mechanical demands,
  manufacturing/assembly, quantity, region, and cost basis.
- [ ] P6.2 Build extraction into that schema with a model adapter. Record the
  model, prompt version, input, and validated output. Reject malformed fields.
- [ ] P6.3 Preserve the difference between user statements, engineering
  derivations, suggested defaults, and unknowns. Do not invent numerical limits
  because a brief says "strong", "cheap", or "high temperature".
- [ ] P6.4 Ask the smallest set of questions that could change the shortlist.
  Prioritize missing geometry, duty conditions, manufacturing compatibility,
  and mandatory limits before preferences.
- [ ] P6.5 For any derived numerical requirement, use an explicit calculation
  with units, assumptions, and a declared validity range. The reviewer validates
  each supported derivation. Otherwise request the requirement from the engineer.
- [ ] P6.6 Let the engineer inspect and correct the proposed specification before
  treating inferred requirements as confirmed. Save each revision with its origin.
- [ ] P6.7 Have the model invoke the deterministic selection functions and explain
  their returned evidence. Numerical qualification stays in the selection engine.
- [ ] P6.8 Check explanations against returned observations and constraint
  results. Omit unsupported claims and expose contradictions or unresolved inputs.
- [ ] P6.9 Treat documents and web content as data, not instructions. Test that
  embedded requests cannot change constraints, trigger external actions, or
  override evidence rules. Constrain ingestion URLs and file access.
- [ ] P6.10 Measure missed constraints, unnecessary questions, unsupported
  requirements, and successful clarification on the development cases.

Completion: the engineer can see why a requirement exists, change it, and obtain
an updated comparison. An incomplete brief produces useful questions or a
clearly provisional result.

## Phase 7. Make sourcing and production constraints useful

Owner: Joshua, with supplier/procurement input coordinated by the owner. Effort
allowance: two to four working days, excluding time waiting for responses.

- [ ] P7.1 Map every shortlisted grade to a manufacturer product page or a
  distributor listing with evidence of exact grade identity. A generic material
  family page may support discovery but is not an exact product match.
- [ ] P7.2 Attach product form, dimensions, processing options, region served,
  ordering or quotation route, and the date each claim was verified.
- [ ] P7.3 Record price only with currency, unit, quantity, form, and date. Record
  lead time, minimum order, sample availability, and stock status only when
  supported. Preserve "unknown" and "quote required" as useful states.
- [ ] P7.4 Define separate sourcing states: manufacturer-listed, sample-offered,
  distributor-stock-reported, supplier-quoted, and customer-qualified. None implies
  the others, and an available sample does not establish volume capacity.
- [ ] P7.5 Create a supplier question sheet for unresolved production issues:
  required annual volume, batch consistency, tolerances, processing yield,
  certifications, change notification, capacity, and continuity of supply.
  The owner decides when to send it and supplies the actual project context.
- [ ] P7.6 Capture written supplier responses as dated evidence with their scope
  and permission to share. Do not infer a grade's production capacity from the
  manufacturer's general company capacity.
- [ ] P7.7 Compare cost on the engineer's relevant basis where evidence permits:
  delivered substrate or finished part, including necessary processing and
  expected yield. If only raw material prices are known, state that limitation.
- [ ] P7.8 Define source-specific freshness rules and expired-claim behavior.
  Recheck volatile availability before the engineer acts; retain the original
  snapshot for historical reproducibility.

Completion: every shortlisted grade has an exact sourcing route or an explicit
unresolved sourcing gap. The output distinguishes technical fit, commercial
availability, and production qualification.

## Phase 8. Expose the service through MCP

Owner: Joshua. Effort allowance: three to five working days.

Use the [official SDK](https://github.com/modelcontextprotocol/python-sdk) and
validated [tool schemas and structured outputs](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).
Start with local stdio; introduce Streamable HTTP when a hosted pilot needs it,
following the [transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports).
Keep protocol handling in an adapter around the tested core functions.

### Initial tool contracts

Names are provisional until the integration spike; freeze them for the pilot.

| Tool | Input | Output |
| --- | --- | --- |
| `prepare_requirements` | Brief and any supplied structured facts | Draft specification, origins/assumptions, and prioritized questions |
| `search_materials` | Validated specification, catalogue version, result limit | Supported and provisional candidates, exclusions, gaps, and ranking components |
| `get_material` | Grade or variant ID | Identity, property observations, conditions, and source references |
| `compare_materials` | Grade IDs and specification | Per-constraint results and explicit preference tradeoffs |
| `get_supplier_offers` | Grade/variant ID, region, and quantity | Exact sourcing links, dated offer facts, and unknowns |
| `get_evidence` | Observation or source ID | Permitted supporting context and original document location |

- [ ] P8.1 Add versioned input and output schemas, bounded result sizes, pagination
  where needed, units, explicit null/unknown meanings, and stable error codes.
- [ ] P8.2 Make `prepare_requirements` reuse Phase 6's model adapter. Mark its
  output as a draft. If a host agent prepares the specification itself, run the
  same deterministic validation before search; do not require duplicate LLM work.
- [ ] P8.3 Include catalogue, task, schema, and engine versions in selection
  results. Return evidence IDs and URLs alongside machine-readable decisions.
- [ ] P8.4 Describe tool boundaries clearly: selection is evidence-based screening;
  unknown is not pass; a supplier listing is not a production commitment.
- [ ] P8.5 Keep tools read-only with respect to supplier and purchasing systems.
  Declare accurate tool annotations, while enforcing actual access and limits
  in code. An annotation is not an access-control mechanism.
- [ ] P8.6 Handle invalid IDs, unsupported units, absent data, source errors,
  model failures, timeouts, and cancellation without inventing successful results.
- [ ] P8.7 Keep source ingestion out of arbitrary agent-controlled URLs. Restrict
  remote fetches to approved sources and guard against redirects into private
  network locations. Keep secrets and confidential source content out of logs.
- [ ] P8.8 Verify the server with an SDK test client and at least two actual MCP
  host/client environments used by pilot participants. Exercise tool discovery,
  schema validation, the complete task flow, errors, and readable citations.
- [ ] P8.9 Measure core query time, whole-conversation latency, model usage, and
  cost per completed task. Set limits against pilot users' actual tolerance.
- [ ] P8.10 Write installation, configuration, catalogue loading, and troubleshooting
  instructions. Test setup from a clean environment with synthetic data.

Completion: an agent can turn a brief into inspected requirements, compare grades,
and return sourcing links using a documented installation. Errors and evidence
gaps remain visible to both the agent and the engineer.

## Phase 9. Give engineers a useful review surface

Owner: Joshua, with pilot-user feedback. Effort allowance: three to five working
days. This can run alongside Phase 8.

- [ ] P9.1 Build the actual comparison workflow as the first screen: brief and
  specification, candidate table, grade detail, and source detail. Use a compact
  work-focused layout rather than a marketing page.
- [ ] P9.2 Let users correct requirements, change preferences, and see the resulting
  comparison. Keep inferred assumptions and unresolved questions visible.
- [ ] P9.3 Show property values with conditions and source links close to the
  relevant cells. Label fail, unknown, and conflicting evidence explicitly;
  do not rely on color alone.
- [ ] P9.4 Show why candidates were excluded and distinguish an empty catalogue
  result from a verified no-match result. Show the scope of the searched data.
- [ ] P9.5 Put supplier links and sourcing status beside the exact grade/variant.
  Show freshness and quote-required states where they affect the next action.
- [ ] P9.6 Export a concise Markdown decision report and a structured JSON record
  carrying versions, requirements, evidence references, exclusions, and next
  validation steps. Add PDF export only if pilot users need it.
- [ ] P9.7 Allow feedback with a reason: useful, missing constraint, wrong grade,
  unsupported property, stale source, or unsuitable sourcing. Preserve the run
  being reviewed instead of overwriting it.
- [ ] P9.8 Verify keyboard navigation, readable tables, loading/empty/error states,
  long grade names, and layout at desktop and narrow widths. Have an engineer
  complete a task without coaching and fix observed friction.

Completion: a user can inspect and challenge a recommendation without reading
implementation details or relying on the conversational explanation alone.

## Phase 10. Evaluate the complete system

Owner: Joshua runs the harness; reviewer/evaluator judges decisions. Effort
allowance: four to six working days, plus reviewer scheduling.

- [ ] P10.1 Freeze the candidate release, catalogue, prompts, model settings, tool
  versions, and protocol. Verify held-out tasks were not used for development.
- [ ] P10.2 Run focused catalogue, constraint, and integration checks. Run existing
  repository checks appropriate to any shared files changed. Confirm public
  packaging excludes restricted data and private briefs.
- [ ] P10.3 Run the held-out tasks and all predefined failure cases. Save full
  candidate outputs, clarification turns, citations, exclusions, elapsed and
  active time, model cost, errors, and any human intervention.
- [ ] P10.4 Execute each comparator with its declared access and budget. Use
  different reviewers or counterbalanced task assignment where possible to
  reduce learning from repeatedly solving the same task.
- [ ] P10.5 Separate fixed-catalogue tests from live-web workflow comparisons.
  Record web dates and changed sources; do not attribute extra catalogue coverage
  to better reasoning without identifying that difference.
- [ ] P10.6 Apply the predefined review rubric. Report per-task outcomes, exact
  numerators/denominators, hard-constraint failures, unknown handling, citation
  support, shortlist usefulness, time, cost, and coverage.
- [ ] P10.7 Run a direct-core versus agent-workflow comparison on the same validated
  specifications. This helps locate errors in requirements interpretation,
  catalogue data, deterministic comparison, or the final explanation.
- [ ] P10.8 Publish the complete local evaluation report, including unsuccessful
  cases and reviewer disagreement. Record whether each Phase 3 target was met.
- [ ] P10.9 Repair failures in development and regression examples. Preserve the
  original report. If decisions are tuned using held-out results, collect new
  held-out cases before making a new performance claim.

Checkpoint C: move to a live pilot when decisive claims are supported, no critical
false passes remain in the evaluated cases, the workflow handles unknowns, and
users gain a material quality or time benefit. If it only matches a general
assistant, investigate the failure source before adding more integrations.

## Phase 11. Run a live pilot and test commercial value

Owner: Joshua with three to five participating engineers. Effort allowance:
five to eight working days spread over two to four calendar weeks.

- [ ] P11.1 Agree pilot scope, data handling, support contact, feedback schedule,
  and what counts as successful use. Establish the user's expected decision
  frequency so repeat use has a meaningful denominator.
- [ ] P11.2 Observe onboarding and the first real task. Record assistance needed,
  misunderstandings, abandoned steps, and whether the result changes their next
  engineering action.
- [ ] P11.3 Ask users to apply the product to at least two distinct tasks when
  their normal work provides them. Separate repeat demand from prompted demos.
- [ ] P11.4 Track what happens after a shortlist: source verification, supplier
  quotation, sample request, engineering review, testing, and final selection.
  These are different outcomes; a click is not a procurement or qualification.
- [ ] P11.5 Review failure reports weekly. Track how much curation and personal
  support each task needs, and whether the same gaps recur across users.
- [ ] P11.6 Test a concrete paid offer with the budget owner. Start with a simple
  team subscription or supported pilot covering named users and reasonable agent
  usage. Determine price from observed value and actual delivery costs.
- [ ] P11.7 Record willingness to pay separately from a paid commitment. Aim for
  at least two independent teams accepting a priced next step or paying for a
  continuation; treat the small sample as directional evidence.
- [ ] P11.8 Calculate cost per completed task: model use, data fees, hosting,
  source maintenance, reviewer time, and user support. Identify which costs
  should decline with repeat use and verify that expectation.
- [ ] P11.9 Summarize qualified repeat use, time saved, errors, support burden,
  sourcing progress, payment evidence, and reasons for declining the product.

Checkpoint D: continue toward a supported beta when users return for real tasks,
some will pay, and the cost of delivering reliable answers supports that offer.
If task frequency is low, test team/API distribution or a paid expert-assisted
workflow. If the central need is supplier qualification, refocus on that workflow
instead of assuming broader materials search will solve it.

## Phase 12. Release, operate, and expand deliberately

Owner: Joshua; specialist input where actual hosting or source contracts require
it. Effort allowance: five to eight working days for an initial supported beta.

- [ ] P12.1 Choose deployment from pilot needs. Keep a supported local option if
  it serves users; add a hosted service when shared data, updates, or customer
  access justify it.
- [ ] P12.2 For remote MCP, implement the current protocol's applicable
  authorization requirements using its
  [official guidance](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization).
  Add TLS, scoped
  access, usage limits, secrets management, and tenant isolation where customers
  upload private data. Test isolation and expired/revoked access.
- [ ] P12.3 Establish retention/deletion controls for customer briefs and documents.
  Make actual model-provider data handling and external-source access clear to
  participating customers before sending their data through those systems.
- [ ] P12.4 Schedule catalogue/source maintenance. Detect changed or removed
  documents, quarantine affected claims, review updated values, and publish a
  new catalogue version with a change log.
- [ ] P12.5 Add backups, a tested restore path, health checks, error reporting,
  usage/cost limits, and rollback for both software and catalogue versions.
- [ ] P12.6 Define an incident response for wrong decisive data: identify affected
  grades and saved runs, correct or withdraw the observation, and inform affected
  customers through the agreed support process.
- [ ] P12.7 Document supported applications, known limits, evidence conventions,
  update cadence, installation, and support. Release source code and catalogue
  content only under their respective permitted terms.
- [ ] P12.8 Package a beta release with synthetic examples, the evaluated version,
  meaningful quality results, and clear limits on what has been demonstrated.
- [ ] P12.9 Prioritize the next application using recorded demand and missed-task
  data. Add one new material family, application, or region at a time with its
  own source-coverage and evaluation checks.
- [ ] P12.10 Revisit learned ranking, property prediction, CAD integration, supplier
  APIs, or automated procurement only when a repeated unmet need justifies them.
  Each capability needs its own evidence and permissions for external actions.

Completion: the service can be installed or accessed, maintained, supported, and
recovered, and customers understand what their subscription or pilot includes.

## 4. Schedule and resource assumptions

The estimates assume one full-time builder, access to a practicing reviewer,
responsive pilot users, and usable source data. They are planning allowances,
not delivery promises. Recruitment, supplier responses, and data agreements can
extend calendar time independently of engineering effort.

| Milestone | Indicative calendar window | Evidence required |
| --- | --- | --- |
| Confirm application and manual usefulness | Weeks 1-3 | Checkpoints A and B |
| Working local demonstration | Weeks 4-6 | Reviewed catalogue, selection core, brief workflow, first MCP task |
| Evaluated private pilot | Weeks 7-10 | Comparison view, integrations, held-out report, checkpoint C |
| Live usage and payment decision | Weeks 10-14 | Repeat real use, actual cost data, checkpoint D |
| Supported beta | Weeks 12-16, if justified | Deployment, maintenance, support, and release checks |

Some activities overlap, but one builder cannot do every implementation phase in
parallel. Re-estimate after the manual pilot and again after the catalogue is
working. Do not compress independent review to meet an arbitrary date.

### Cost worksheet to complete in Phase 0 and revisit in Phase 11

| Cost | How to estimate it |
| --- | --- |
| Engineering | Actual builder days against the phase allowances |
| Technical review | Quoted review hours for schema, derivations, curated values, and held-out decisions |
| Data access | Source-specific subscription/API/redistribution quotes for intended use |
| Model usage | Measured cost per completed task, including retries and clarification |
| Infrastructure | Local-first baseline; actual hosted, storage, and monitoring quotes when needed |
| Maintenance | Measured minutes per changed source and affected grade, multiplied by observed change frequency |
| Customer support | Actual onboarding and support time per team |
| Materials testing | Customer-agreed sample and lab costs if a later validation study requires them |

Do not treat physical qualification testing as included in the software pilot
unless its scope, owner, and budget are explicitly agreed.

## 5. Risks and decisions that can change the plan

| Observed problem | Response |
| --- | --- |
| Critical property conditions are usually absent | Narrow the application, obtain supplier data, or provide evidence retrieval with explicit gaps |
| Data rights or maintenance costs make broad aggregation impractical | Use permitted supplier partnerships or customer-owned catalogues; retest the business case |
| Engineers cannot derive requirements without detailed system design | Support confirmed specifications and selected validated calculations; narrow the task boundary |
| General assistants already solve the task adequately | Identify a measurable specialist advantage or stop expanding this application |
| Useful answers require extensive bespoke expert work | Price and test an expert-assisted service before claiming software economics |
| Users like the demo but rarely return | Reassess decision frequency, buyer, and distribution before growing coverage |
| Supplier links rarely lead to viable volume supply | Focus the next iteration on grade availability, qualification, and sourcing evidence |
| Unsupported claims appear in model explanations | Restrict explanations to verified result fields, improve validation, and rerun fresh evaluation |
| Catalogue freshness changes conclusions | Version evidence, mark stale claims, and measure update impact on saved decisions |

## 6. First ten actions

1. Finalize the one-page charter using the working assumptions in this plan.
2. Set the initial budget ceiling and recruit the technical reviewer.
3. Identify and contact five to eight relevant engineers through existing
   relationships; start scheduling task walkthroughs.
4. Collect three real briefs immediately and begin gathering the full task set.
5. Confirm whether ceramic substrates are the best starting application.
6. Build the source register and verify intended data uses.
7. Curate ten grades manually across at least three manufacturers.
8. Produce and review three manual recommendation reports.
9. Write the selection evaluation protocol and separate development from held-out
   tasks before tuning the service.
10. Make the checkpoint B decision, then build the smallest complete path from
    a structured requirement to a sourced, reproducible shortlist.

The first substantial engineering milestone is one trustworthy end-to-end
selection. Broad catalogue coverage and additional integrations follow evidence
that this workflow improves a real decision.

## 7. Sources and implementation references

These references inform the plan; vendor descriptions are not independent
evidence of product effectiveness. Recheck current versions and source terms
when implementing. Reviewed or identified on 8 October 2026.

- [S1: Ansys Granta Selector documentation](https://ansyshelp.ansys.com/public/Views/Secured/Granta/v261/en/Selector/sel_edu/selector.html): existing selection, substitution, and comparison capabilities.
- [S2: Total Materia Optimizer](https://www.totalmateria.com/en-us/horizon/optimizer/): existing multi-criteria materials ranking and tradeoff workflow.
- [S3: CoorsTek brochures and datasheets](https://www.coorstek.com/en/resources/brochures-datasheets/): candidate manufacturer source directory; source access and reuse remain to be checked per document.
- [S4: Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk): supported SDK and implementation documentation; choose a tested release during the architecture spike.
- [S5: MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools): reference for tool schemas and structured responses for this published protocol version.
- [S6: MCP transports specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports): reference for local stdio and Streamable HTTP for this published protocol version.
- [S7: MCP authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization): reference to verify against the protocol version selected for a hosted implementation.
