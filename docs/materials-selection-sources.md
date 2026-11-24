# Materials Selection: Source Inventory

Inspected 13 October 2026. Scope: a small source-feasibility investigation, not a
downloaded catalogue or legal opinion. No paid access, supplier contact, account
creation, bulk scraping, or manufacturer-data redistribution was performed.

## Admission decision

Four exact alloy/grade candidates were inspected through manufacturer documents:
Hydro 6061-T6 and 6082-T6 extrusions, Ensinger TECANAT natural, and Ensinger
TECAPEEK natural. Begin with these four reference candidates rather than assuming
15-30 grades are necessary. This is two broad material classes, not broad market
coverage. A CoorsTek ceramic page is an excluded follow-up lead.

None is currently approved by this project for commercial catalogue ingestion,
redistribution, or public numeric display. Public access is not permission for
those uses. The immediate software demo uses authored synthetic records and
fictional grade names; these must never be presented as manufacturer data. An
actual engineering shortlist still requires admitted real evidence.

The inventory below records document identity, inspection findings, and next
actions. It deliberately does not reproduce property tables or source files.
Links are research citations, not representations of an approved sourcing offer.

## S-H6061: Hydro 6061 extrusion

- Candidate: Hydro 6061-T6, extruded stock; keep T6511 and special tempers separate.
- Source: [Alloy 6061 PDF](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf).
- Discovery/supply route: [North America alloy index](https://www.hydro.com/us/us/aluminum/products/extruded-profiles/north-america-resources/north-america-alloy-data-sheets/).
- Document revision: 2019/01 (2/2019), shown on page 2; checked 2026-10-13.
- Inspection: both pages' extracted text; page 2 mechanical/physical table and
  footnotes. The table includes tensile minima by temper/thickness and separately
  labels typical conductivity. The source warns about strength after welding.
- Applicability: extrusion, not rolled plate; section thickness is tied to the
  tension specimen. Test temperature/method is not fully supplied in the selected
  row. Do not infer these from unrelated thermal-property headings.
- Storage/display/redistribution: not approved; R-H below. No local source copy.
- Gaps: visual table verification before ingestion, current product specification,
  exact orderable stock form, quantity, location, stock, price, and rights basis.
- Demo: DEMO-01; exact commercial offer remains unverified.

## S-H6082: Hydro 6082 extrusion

- Candidate: Hydro 6082-T6, extruded stock; do not merge with 6061 or T6511.
- Source: [Alloy 6082 PDF](https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6082_revise_1.pdf).
- Discovery/supply route: the North America alloy index above.
- Document revision: 2019/02 (3/2019), page 2; checked 2026-10-13.
- Inspection: both pages' extracted text; page 2 table contains thickness bands,
  tensile minima, typical conductivity, and a separate reference-standard block.
  Rounded unit pairs and thickness boundaries must not become independent data.
- Applicability: retain the selected temper, stock thickness and table block;
  do not combine reference EN limits with a different listed specification.
- Storage/display/redistribution: not approved; R-H. No local source copy.
- Gaps: visual verification, specification confirmation, orderable product and
  region, stock, price, quantity, and rights basis. Older revision does not establish
  current availability. Demo: DEMO-01.

## S-EPC: Ensinger TECANAT natural

- Candidate: TECANAT natural, unfilled PC stock shapes, not an arbitrary PC resin.
- Source: [TECANAT natural datasheet](https://www.ensinger-online.com/modules/public/sheet/createsheet.php?FILENAME=TECANAT_natural_0.PDF&FL=0&SID=1346&ZOOM=1.2).
- Discovery/product route: [US product page](https://www.ensingerplastics.com/en-us/shapes/polycarbonate-tecanat-natural).
- Document date/version: 2023/07/19, AF; checked 2026-10-13.
- Inspection: full one-page extracted text, including reference specimen and
  disclaimer. Mechanical, thermal, and electrical properties have differing
  context. Values are guidelines, not guaranteed specification limits.
- Acquisition issue: product-page direct retrieval timed out; the manufacturer
  PDF was readable. Text extraction displaced superscripts, so electrical
  exponents and compound units require visual checks before numeric ingestion.
- Storage/display/redistribution: not approved; R-E. No local source copy.
- Gaps: confirmed regional variant, long-duration performance under actual load,
  chemical/impact conditions, exact supply form, and rights basis. Demo: DEMO-02.

## S-EPEEK: Ensinger TECAPEEK natural

- Candidate: TECAPEEK natural, unfilled PEEK stock shapes; not TECAPEEK IM or a
  raw-resin grade. Keep regional source identity explicit.
- Source: [manufacturer-linked datasheet](https://www.ensinger-online.com/modules/public/sheet/createsheet.php?FILENAME=TECAPEEK_natural_18.PDF&FL=18&SID=694&ZOOM=1.0).
- Discovery/product route: [India product page](https://www.ensingerplastics.com/en-in/shapes/peek-tecapeek-natural), Downloads section.
- Document date/version: 2023/07/19, AG; checked 2026-10-13.
- Inspection: complete one-page extracted text and product technical details.
  Service temperature, heat distortion, and melting point are separate fields;
  electrical observations include their own temperature/humidity/specimen context.
  The disclaimer labels values as guidelines rather than guaranteed limits.
- Acquisition: public manufacturer page to its linked PDF; no login or payment.
- Storage/display/redistribution: not approved; R-E. No local source copy.
- Gaps: visual exponent checks, regional equivalence, loaded lifetime/creep,
  actual stock/price/form, and permission basis. Demo: DEMO-02.

## S-CALN: CoorsTek ceramic lead, excluded

- Candidate labels found: AlN 180, AlN-HP, AlN-HTC; these are distinct, not aliases.
- Lead: [Aluminum Nitride page](https://www2.coorstek.com/en/materials/aluminum-nitride/).
- Revision: not established. Search-indexed manufacturer content inspected on
  2026-10-13; direct retrieval failed, so this is not a verified catalogue source.
- The indexed table lists grade-specific density, thermal, and electrical rows.
  Its conductivity unit appears as W/m rather than a complete conductivity unit.
  Do not silently supply the missing temperature dimension or transfer a
  measurement at one temperature to a different requested temperature.
- Storage/display/redistribution: not approved; R-C. No local copy or numeric import.
- Next action: retrieve a revisioned primary datasheet and check its rendered
  headers, units, conditions, exact product, and permissions. DEMO-03 uses this
  only to demonstrate a visible coverage gap, not a numeric recommendation.

## Rights and access register

These are conservative project admission decisions based on inspected terms, not
a legal determination about the copyright status of individual facts. Resolve
the intended use before importing or publishing source-derived records. No
request for permission or acceptance of a new agreement has been sent.

| ID | Terms inspected | Observed limitation and project decision |
| --- | --- | --- |
| R-H | [Hydro legal notice](https://www.hydro.com/us/global/legal-notice-terms-and-conditions/), updated 2024-05-15 | Authorization described as personal/non-commercial; commercial reuse and public distribution not established. No ingestion approval. |
| R-E | [Ensinger US terms](https://www.ensingerplastics.com/en-us/general-terms-of-website-use), [India terms](https://www.ensingerplastics.com/en-in/legal-disclaimer-and-terms-of-use-india), [international notice](https://www.ensingerplastics.com/en/legal-notices) | Reproduction restrictions vary by regional page. International notice also restricts hyperlinks without consent. Resolve regional applicability and intended linking/display use; do not assume the PDF endpoint grants a reuse licence. |
| R-C | [CoorsTek conditions](https://www.coorstek.com/en/legal-conditions-privacy-policy/), conditions dated 2016-07-12 | Inspected indexed terms authorize personal/non-commercial use, with copying and distribution restrictions. Direct retrieval failed. No ingestion approval. |

## Coverage and immediate implementation

| Demo | Evidence route inspected | Current implementable scope | Remaining real-data gap |
| --- | --- | --- | --- |
| DEMO-01 bracket | S-H6061, S-H6082 | Synthetic observations for minima, thickness, units, provenance | Permissions and exact applicability/product verification |
| DEMO-02 cover | S-EPC, S-EPEEK | Synthetic guidelines and missing requirements | Permissions and application-relevant conditions |
| DEMO-03 heat spreader | Metal/polymer references; S-CALN excluded lead | Authored no-supported-match fixture and explicit coverage gap | Admitted ceramic evidence and full electrical/thermal context |

MVP-02 establishes the inventory and revises the immediate demo scope; it does not
complete real catalogue ingestion. MVP-04 must resolve at least one usable
real-data route (a permissioned source or appropriately licensed user-supplied
evidence), or record that the build remains synthetic-only. An inaccessible or
restricted source is excluded rather than used as a reason to halt schema work.

Before admitting a source, record exact version/date and content hash of any
permitted retained copy, grade/variant identity, source location, original units,
measurement conditions, evidence basis, and separate storage/display/distribution
decisions with their basis. Missing permission is unknown, not allowed. A source
reference is not a stock guarantee or an orderable offer. Keep real record-level
data out of the public repository and public tests synthetic.
