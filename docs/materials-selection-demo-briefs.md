# Materials Selection: Demonstration Briefs

Version 1, 13 October 2026. Self-authored software demonstrations, not customer
cases, validated engineering answers, or evidence of market demand. All thresholds
below are invented task inputs, not recommendations or derived design limits.

The [source inventory](materials-selection-sources.md) separates inspected
manufacturer references from approved catalogue inputs. Start implementation with
fictional fixtures. Do not attach real grade names to fictional property values.

## DEMO-01: Bolted laboratory sensor bracket

### Brief

"Compare existing materials for a non-safety-critical sensor bracket machined
from 10 mm extruded stock. It is bolted, not welded, and used indoors near room
temperature. For this preliminary screen, I want a documented minimum tensile
yield strength of at least 200 MPa. Prefer lower mass at unchanged geometry, and
show machining and sourcing considerations. Do not approve the finished design."

### Supplied facts and limits

- Function: support a laboratory sensor; commercial stock, followed by machining.
- Process: extrusion, machining, bolting; no welding or further heat treatment.
- Stock section thickness: 10 mm, not a statement of final part dimensions.
- Mandatory evidence: a published minimum for tensile yield strength. A typical
  tensile strength, ultimate strength, or flexural strength is not a substitute.
- Preliminary threshold: at least 200 MPa. Room temperature is qualitative;
  record the source's temperature or its absence, without inventing 23 degrees C.
- Preferences: lower density at identical geometry, machinability, sourcing route.
  No numeric cost, mass, delivery-date, or regional requirement is supplied.

### Questions and assumptions

Ask about loads, geometry, fatigue, tolerable deflection, environment, fasteners,
surface treatment, tolerances, and quantity before claiming design suitability.
Confirm whether a datasheet limit is sufficient for this preliminary screen or
whether a purchase specification/certificate is required. The demo does not infer
a yield limit from a load, or turn this screen into structural verification.

### Evidence route and intended behavior

Hydro 6061-T6 and 6082-T6 extrusions are inspection candidates S-H6061 and S-H6082,
not approved data imports. Their tables distinguish thickness-dependent minima
from typical physical properties. Preserve each alloy, temper, source revision,
and original units. Do not borrow a T6511 or special-temper claim just because
it appears on the same sheet. The referenced sheets are North American sources,
not evidence of stock in a user's country. See the linked source inventory.

Show each requirement's supporting observation and any unresolved applicability.
If the engineer raises the threshold, a published lower bound below that threshold
does not prove the material's actual strength is below it: report insufficient
evidence unless an applicable upper bound or other evidence establishes failure.
Equivalent units must produce equivalent checks. Unknown density cannot win a
minimum-mass comparison. Fewer than three options is an acceptable result.

### Acceptance cases

- Preserve the supplied 200 MPa limit and 10 mm stock thickness as supplied inputs.
- Reject substitutions of ultimate/flexural strength for tensile yield strength.
- With synthetic evidence, distinguish a sufficient lower bound, an insufficient
  lower bound, an incompatible thickness, and missing test conditions.
- Changing to a welded part invalidates any automatic transfer of unwelded limits.
- Report sourcing gaps and missing price/stock, without contacting suppliers.

## DEMO-02: Hot equipment cover with incomplete requirements

### Brief

"I need a lightweight plastic cover near a hot laboratory instrument. It should
be tough, easy to machine, and ideally transparent. What materials should I use?"

### Supplied facts and limits

- Function: equipment cover; plastic requested; machining intended.
- Preferences: low mass, toughness, machinability, transparency.
- No numerical temperature, load, impact, thickness, chemical exposure, fire,
  electrical, cost, quantity, or geography limit has been supplied.

### Questions and assumptions

Ask first for maximum continuous/peak material temperature and exposure duration;
then whether transparency is mandatory, and what chemicals, impact, fire, or
electrical requirements apply. Do not convert "hot" into a service-temperature
limit, "tough" into a tensile-strength requirement, or "lightweight" into density.

For a repeatable follow-up path only, the fictional engineer replies: "Maximum
continuous exposure is 110 degrees C in dry air. Transparency is preferred, not
mandatory. This is an initial comparison using guideline values, not a guarantee
of performance. Chemical cleaning and impact requirements are still unknown."
Mark these as supplied follow-up facts, not inferred facts from the initial brief.

### Evidence route and intended behavior

Ensinger TECANAT natural and TECAPEEK natural are reference candidates S-EPC and
S-EPEEK. Their source warnings and test context matter: a service-temperature
guideline is not proof of stiffness, creep life, or impact performance at that
temperature. Do not substitute a melting point, glass transition, or heat
distortion test for continuous-use evidence. Shape grades are not automatically
interchangeable with resin grades or injection-moulded variants.

Initially return clarification and provisional leads, not qualified matches.
After the follow-up, keep absent environmental conditions and unverified
application performance visible. An opaque candidate can remain an alternative
while transparency is only a preference; making it mandatory must change the
requirements without silently relaxing them. Source permissions are unresolved.

### Acceptance cases

- Initial extraction contains no invented numeric limits or compulsory transparency.
- User corrections reach the saved specification, with provenance preserved.
- Missing/ambiguous service-temperature evidence stays unknown.
- Guidelines cannot pass a requirement for guaranteed performance.
- Explain tradeoffs without inventing impact performance, cost, or an exact offer.

## DEMO-03: Heat-spreader screen with no supported match

### Brief

"Compare solid, uncoated stock materials for an electrically insulating heat
spreader. For this preliminary reference screen, require thermal conductivity of
at least 100 W/(m*K) at 25 degrees C, density no greater than 2 g/cm^3, and volume
resistivity of at least 10^10 ohm*cm at 25 degrees C. Typical values are acceptable
for screening only. Do not change the limits to make something fit."

### Supplied facts and limits

- Application: solid heat spreader; no coatings, foams, or assemblies in this demo.
- Three mandatory screening constraints, with units, temperatures, and acceptable
  evidence basis as stated above. Density temperature is not supplied.
- No voltage, dielectric withstand, thickness, heat flux, joining process,
  humidity, operating life, or actual operating-temperature range is supplied.
- Volume resistivity is not dielectric strength, and neither alone qualifies
  electrical safety. No design approval is requested or provided.

### Questions and assumptions

Ask for the operating environment, electrical requirements, geometry, interfaces,
and whether any limit is negotiable. Do not presume that conductivity measured
at 20 degrees C applies at 25 degrees C, or infer dielectric withstand from
resistivity. Proposed changes require an explicit edited task version.

### Evidence route and intended behavior

The initial four reference candidates span metals and polymers, not the entire
materials space. S-CALN is a ceramic follow-up lead, excluded from initial
numeric comparisons because its direct retrieval and unit context need checking.
This omission must be visible, not disguised as an exhaustive search.

The deterministic no-match expectation belongs to the fictional fixture set:
one candidate fails density, another fails conductivity, and a third lacks
applicable resistivity evidence. Thus none is a supported match. This does not
assert that no real material exists. Every failed/unknown constraint remains
visible; a good preference score cannot rescue a failed mandatory requirement.

### Acceptance cases

- Zero supported matches is a valid completed report, not a model error.
- Separate known screening failures from unknown or conflicting evidence.
- An out-of-coverage ceramic lead stays unranked until exact evidence is admitted.
- A subsequent relaxed-density task is a new explicit version, not a hidden fix.
- Surface a source's malformed unit for review; never silently repair it.

## First implementation slice

Start with DEMO-01's structured inputs, synthetic grades and sources, and exact
provenance. Establish storage round trips before implementing comparison. Carry
all three briefs into later requirements, UI, and MCP checks. These acceptance
cases describe expected software behavior; they have not yet been executed end
to end. MVP-11 will record actual demonstration results.
