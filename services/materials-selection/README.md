# Materials selection service

This local Python service validates versioned evidence catalogues, saves
immutable SQLite snapshots, and compares manually screened candidates on a
user-defined material index. It does not search the web,
recommend materials, call a model, or provide a UI/MCP server yet. The existing
Julia package is not imported or modified.

## Run from the repository root

Tested with Python 3.14.6. The nine required runtime packages, including transitive
dependencies, are pinned in `requirements.txt`. The environment and databases
remain in ignored local directories; no credentials are needed.

```bash
python3 -m venv tmp/materials-selection-venv
tmp/materials-selection-venv/bin/python -m pip install -r services/materials-selection/requirements.txt

PYTHONPATH=services/materials-selection tmp/materials-selection-venv/bin/python -m eka_materials validate services/materials-selection/examples/synthetic-catalogue.json

PYTHONPATH=services/materials-selection tmp/materials-selection-venv/bin/python -m eka_materials snapshot services/materials-selection/examples/synthetic-catalogue.json --db tmp/materials-selection-demo.sqlite

PYTHONPATH=services/materials-selection tmp/materials-selection-venv/bin/python -m unittest discover -s services/materials-selection/tests -v
```

`validate` performs no writes. `snapshot` returns the content hash; passing that
hash to `show HASH --db tmp/materials-selection-demo.sqlite` reads the stored
snapshot without modifying the database. `schema` prints the Pydantic-generated
JSON Schema. Invalid input or insufficient permissions returns a nonzero exit
code. CLI commands run offline after dependency installation.

The example contains three fictional grades, nine authored observations, two
synthetic sources, three task slices, and one explicitly fictional offer. It is
not an extracted manufacturer catalogue. Values are intentionally artificial and
include conflicting evidence; they cannot be used in engineering. The three task
slices are not full implementations of the [demo briefs](../../docs/materials-selection-demo-briefs.md).

## Compare a shortlist on a material index

Use `rank-index` after screening. It takes a worksheet with a stated objective,
the starting equations and assumptions behind one material index, and the
evidence for each candidate. It can work with family-level records as entered.
The worksheet is independent of the grade catalogue and creates no snapshot.

Try the [fictional worked example](examples/synthetic-index.json) from the repository root:

```bash
PYTHONPATH=services/materials-selection tmp/materials-selection-venv/bin/python -m eka_materials rank-index services/materials-selection/examples/synthetic-index.json
```

The example minimizes the mass of a tie rod under a fixed tensile force.
A and B both outperform C on that index. Their ranges overlap each other.
D's unresolved screen keeps it out of the comparison.

To use your own index:

1. Copy the example to an ignored local path such as
   `data/local/materials-selection/my-index.json`. Set the objective, derivation
   and direction for your case. Replace the example exponents with the ones in
   your derivation. The calculator supports products of positive properties
   raised to fixed powers, including fractional and negative powers.
2. Replace the fictional candidates with your screened records. Preserve each
   record's identity and enter your screening outcome and reason. For each
   property, enter the source range, original unit, evidence basis, conditions
   and your judgment of applicability. In `source`, identify the database or
   document, edition/revision, record, and property or table. Enter only values
   you have permission to use locally.
3. Run the same command with the path to your copy. Add `--json` to inspect
   the source rows, conditions, screen decisions, and reasons alongside the
   results. This command reads the local worksheet and writes to standard output.

The six property keys and their index units are defined in
[the unit registry](eka_materials/units.py). The output uses those units
consistently across candidates. Each input range contributes its two extremes
in the order implied by its exponent. The resulting interval encloses the index
values allowed by the entered ranges. Endpoints may combine extremes that do
not occur together. They carry no probability or guarantee.

A comparison favours a candidate only when the ranges are separated in the
requested direction (relative tolerance `1e-12` at the boundary). Overlap
leaves the order unresolved. A failed, unknown or conflicting manual screen
prevents scoring. Missing terms, unresolved applicability, multiple potentially
applicable observations, and one-sided bounds each leave the candidate unranked.
A single typical range may support exploratory ranking after a manual screen.
The group supplies evidence for hard limits and checks the index assumptions.

## Schema v1

| Record | Identity and purpose |
| --- | --- |
| Family | Broad classification; never a commercial-grade identity |
| Grade | Manufacturer and designation, linked to a family |
| Variant | Grade plus form, processing, and temper; observations attach here |
| Source | URL, revision or explicit unknown, access date, optional retained-copy hash, source kind, rights basis |
| Observation | Property, original quantity/unit, evidence basis, conditions, source and exact locator |
| Task | ID/revision, brief, constraints, preferences, unanswered questions |
| Offer | Exact variant/product URL, supplier, dated source/locator; unknown availability/region/quantity remain unknown |

IDs are stable strings provided by an importer, unique across a catalogue.
References must resolve to the correct record type. Two variants do not become
the same because their names, compositions, or values resemble one another.
Conflicting observations keep separate IDs and sources; storage does not choose
a winner. Source and task revisions contribute to snapshot identity.

Supported numeric properties are density, tensile yield strength, tensile
modulus, thermal conductivity, service temperature, and volume resistivity.
Pint checks dimensions and conversions. Original units and numeric bounds remain
stored; canonical values are derived on demand. Temperature conditions are in
kelvin, thickness in millimetres, and humidity in percent. Absent conditions stay
null; they are not filled from defaults or neighboring rows.

`NumericValue` distinguishes a point, closed interval, inclusive lower bound,
inclusive upper bound, and missing value with an explicit reason. Strict/open
bounds are not supported yet and must not be imported as inclusive bounds. A
missing number cannot become zero. Non-finite values, numeric strings, booleans,
reversed bounds, unexpected fields, and incompatible units are rejected. Do not
replace malformed source units with guesses merely to satisfy validation.

Evidence bases distinguish typical values, guidelines, specified limits,
measurements, and unstated basis. Constraints preserve supplied, assumed, or
derived origins; derived inputs require written derivations, which this layer
stores but does not calculate or verify. Categorical requirements remain in the
brief/questions until a typed categorical model is implemented. No information
should be silently reduced to an unsupported numerical comparison.

## Storage and permissions

SQLite stores complete canonical JSON snapshots keyed by SHA-256. Sorting record
collections by ID makes their input order irrelevant. A changed observation,
source, permission, or task creates a new hash rather than overwriting history.
Reads verify the hash and revalidate the schema. This initial storage format
prioritizes a reproducible round trip; indexed grade queries and migrations are
later work, not implied features.

Each source records separate retain/display/redistribute decisions. Unknown and
prohibited are denied. Snapshot writes require retain permission for every
source; CLI display requires display permission. The schema can inspect an
unapproved record without admitting it to storage. Recording `allowed` is an
importer's explicit assertion backed by the recorded basis, not a legal finding
or automatic approval. Redistribution checks are exposed for a future export
adapter; no redistribution command is implemented.

No live documents are fetched by this layer, including URLs found in source text.
Source strings are data. Keep real data in ignored local paths and follow the
[source admission decisions](../../docs/materials-selection-sources.md).

## Next work

MVP-05 still needs automatic applicability and constraint checks on the
versioned grade catalogue. The index worksheet currently takes screening
decisions as input. MVP-04 continues to track real-data admission. Normalization is
not comparison: a lower bound below a requested minimum cannot by itself prove
failure, nor can typical data establish a guaranteed minimum. UI, brief extraction,
shortlist explanations, and MCP integration follow their task dependencies.
