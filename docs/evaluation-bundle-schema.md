# Evaluation bundle schema

Status: internal research schema, version 1. It is additive and does not change
any frozen schema-v1 recovery, label-sensitivity, system-holdout or element-pair
bundle.

The `EkaCompositions.Research.EvaluationSuite` module writes and validates a
portable directory with this shape:

```text
run.toml
inventory.toml
rankings.tsv
metrics.tsv
runtime.tsv                 optional; excluded from deterministic identity
provenance/...              exact captured inputs, code, locks and protocol
memberships/...             exact split memberships
```

## Identities

`run_id` is SHA-256 over a sorted canonical TOML representation of the complete
`scientific` table. It deliberately excludes output paths, wall-clock timestamps,
host/runtime measurements and the descriptive execution environment. The table
binds:

- dataset identity, version, retrieval metadata and input hashes;
- audit algorithm and implementation hashes;
- code commit, dirty flag, source-tree digest, relevant source hashes and
  dependency-lock hashes;
- protocol ID, protocol bytes and hash;
- split algorithm, label policy and membership hashes;
- candidate definition and exclusion counts;
- method configurations and the role of every seed;
- metric algorithm/version, ordered budgets, grouping rule and denominators.

`inventory_sha256` hashes `inventory.toml`. That inventory binds every
deterministic output and every declared provenance artifact. `runtime.tsv`, when
present, is named under `excluded_files` and is never part of either identity.
This means two same-environment reruns may have different timings while retaining
the same run and deterministic-inventory identities.

Internal hashes detect ordinary corruption. They cannot establish historical
identity if an editor rewrites a file and every hash that points to it. A report
or release record must therefore preserve at least the externally published
`run_id`; preserving `inventory_sha256` additionally fixes non-scientific output
diagnostics such as coverage strings. `validate_bundle` accepts both expected
values for this purpose.

## Output tables

`rankings.tsv` contains one complete, canonical composition ranking for every
`(split_id, method)` pair. Its fixed columns are:

```text
split_id method rank composition score tie_key coverage observed_relevant
```

The file is UTF-8 tab-separated text with LF endings and a trailing LF. Ranks are
one-based and contiguous. Formula strings must already be canonical. A ranking
has either finite numeric scores for every candidate or an empty score for every
candidate. Numeric scores are nonincreasing. The tie key is a lowercase SHA-256
digest. All methods in one split must receive the same candidate and relevant
sets.

`metrics.tsv` prepends `split_id` and `method` to every field documented in
[Evaluation metric semantics](evaluation-metrics.md). The writer ignores
caller-supplied metric values and computes them from the saved ranking and
evaluator-owned relevance membership. The validator independently rebuilds the
entire metrics file byte for byte from `rankings.tsv`; missing, extra, reordered,
wrong-typed or edited rows fail validation.

## Failure behavior

Schema tables use exact key sets. Missing and extra keys, wrong types, unsafe
relative paths, undeclared artifacts, duplicate artifact declarations, hash
mismatches, incomplete rankings and unknown methods are errors. The writer:

1. validates every in-memory input before reserving the destination;
2. refuses an existing file, directory or dangling symlink;
3. requires the parent directory to exist;
4. reserves the output with `mkdir`; and
5. removes only that newly reserved directory if a later write fails.

The module has no CLI entry point and is internal pending a prospectively frozen
real-data protocol.
