# API reference

Every exported name, grouped by the stability tier it belongs to. The tiers, and
what each one promises, are defined in
[API stability](reference/api-stability.md) and enforced by `test/test_api.jl`.
Anything not listed here is internal, regardless of visibility.

```@meta
CurrentModule = EkaCompositions
```

```@docs
EkaCompositions
```

## Stable

Available for the life of 0.1.x. Signatures and observable behaviour will not
change incompatibly; new keyword arguments with defaults may be added.

### Compositions

```@docs
Composition
formula
species
similarity
```

### Ranking

```@docs
AbstractRankingMethod
ScoreRanking
SimilarityRanking
ranking_value
rank_compositions
rank_by_score
rank_by_similarity
```

### Databases

```@docs
query_compositions
database_info
validate_database
import_compositions
import_tsv
```

## Stable command-line behaviour, experimental Julia signature

These back the frozen command-line interface. The **CLI behaviour is stable** for
0.1.x. The **Julia signatures are not**: they may gain, lose or reorder arguments
in a 0.1.x release, because they exist to serve the CLI and the research
protocols rather than as a general-purpose library surface.

```@docs
main
benchmark_rankings
benchmark_tsv
audit_mp_snapshot
split_mp_recovery
benchmark_pu
```

## Experimental

Part of the research surface. These may change in any 0.1.x release; a change is
recorded in the changelog rather than in the version number.

```@docs
mp_recovery_splits
load_mp_recovery
pu_rank
pu_metrics
write_synthetic_mp_snapshot
```

## Internal

Everything under `EkaCompositions.Research` — `MPLabelSensitivity`,
`MPSystemHoldout`, `ElementPairModel` and `MPElementPair` — is internal. Nothing
there is exported, no research subcommand is wired into the CLI, and interfaces
may change between any two releases with no deprecation path. They live in the
package so they are precompiled, tested and loaded once, not because they are a
public API. They are deliberately absent from this reference.

## Index

```@index
```
