# Getting started

## Installation

EkaCompositions supports Julia 1.10 and newer. From a repository checkout:

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'
```

The package requires no network access after installation. Queries, tests and the
synthetic examples all run offline.

## Compositions

A [`Composition`](@ref) is a canonical reduced element ratio. Parsing normalises
element order and divides out any common factor, so equality and hashing ignore
both:

```@example intro
using EkaCompositions

composition = Composition("Zn1Mg2")
formula(composition)
```

```@example intro
composition == Composition("Mg2Zn1")
```

```@example intro
Composition("Mg2Zn2") == Composition("MgZn")
```

That normalisation is load-bearing for callers using compositions as dictionary
keys, and it will not change during 0.1.x:

```@example intro
length(Set([Composition("MgZn"), Composition("Zn2Mg2")]))
```

Formulas use valid element symbols and positive integer amounts. Repeated symbols
are combined and counts reduce to the simplest ratio. Parentheses, isotopes,
charges, whitespace and fractional amounts are unsupported.

## Querying a score database

[`query_compositions`](@ref) is a read-only query over an existing SQLite score
database. The examples below use the twelve-row fixture that ships with the
repository for software testing — it is not a set of predictions.

```@example intro
fixture = joinpath(pkgdir(EkaCompositions), "test", "fixtures", "tiny_test.db")

results = query_compositions(fixture; elements=["Al", "Si", "O"], nary=[4], threshold=0.3)

for (composition, score) in results
    println(formula(composition), " => ", score)
end
```

Inspect a database's schema with [`database_info`](@ref), and audit every record
in it with [`validate_database`](@ref).

## Command line

The `eka` executable in `bin/` exposes the same query path plus six subcommands.
Running it with no subcommand performs a stored-score query:

```bash
julia --project=. bin/eka -e Al Si O -n 4 -d test/fixtures/tiny_test.db
```

```text
# Composition, Score
Al2Ba2O7Si1   0.74232
Al2O12Si3Zn3   0.48140
Al1Li1O12Si5   0.41613
Al2Ba3O14Si4   0.39355
Al2O14Si4Sr3   0.34611
```

| Command | Purpose | Guide |
| --- | --- | --- |
| `eka -d PATH [options]` | Query and rank stored SQLite scores. | [Production validation](reference/production-validation.md) |
| `eka import` | Build a new query database from scored TSV records. | [Design notes](reference/design.md) |
| `eka validate` | Audit every record in a SQLite database. | [Production validation](reference/production-validation.md) |
| `eka benchmark` | Evaluate binary-labelled rankings at fixed budgets. | [Benchmark contract](reference/benchmarking.md) |
| `eka audit-mp` | Verify and group an MP-shaped snapshot. | [MP pilot](reference/mp-pilot.md) |
| `eka split-mp` | Generate deterministic PU splits. | [Split guide](reference/mp-recovery-splits.md) |
| `eka benchmark-pu` | Verify splits and evaluate PU methods. | [PU evaluation](reference/mp-pu-evaluation.md) |

Append `--help` to any subcommand. A bare `--help` describes the query options.

The command-line surface is frozen for 0.1.x: the same arguments produce the same
results and the same output format. The Julia functions behind it are not equally
stable — see [API stability](reference/api-stability.md).
