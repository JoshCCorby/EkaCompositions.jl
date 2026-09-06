# Engineering roadmap: documentation, API contract and package quality

Prepared 4 September 2026. This covers software packaging and documentation
quality. It does not propose new science; scientific sequencing lives in the
[recovery roadmap](recovery-roadmap.md), and no item here amends a frozen
protocol.

Tasks 1–4 and 6 are complete. Task 5 is deferred to a version boundary.

## Constraints

These bound every task below. Violating any breaks the package or the
comparability of existing evidence.

**C1. Four protocol documents are content-hash-pinned.** `recovery_protocol()`
(`src/mp_recovery.jl`) reads the document from `docs/` and throws unless its
SHA-256 matches a frozen literal: `mp-recovery-protocol.md`,
`mp-label-sensitivity-protocol.md`, `mp-system-holdout-protocol.md` and
`mp-element-pair-protocol.md`. They are never moved, renamed, reformatted or
edited. A change means a new protocol identifier and a new pin.

**C2. Five `docs/` paths are literal provenance-manifest keys.**
`src/mp_element_pair.jl` records `docs/mp-element-pair-protocol.md` and
`docs/mp-learned-feasibility.md`; `src/mp_system_holdout.jl` records
`docs/mp-recovery-protocol.md`, `docs/mp-label-sensitivity-protocol.md` and
`docs/mp-system-holdout-protocol.md`. Moving one changes manifest keys and
breaks key-for-key comparison with the baselines under `reports/local/`.
`mp-external-score-provenance.md` and `mp-pu-evaluation.md` appear only in prose
and are not constrained.

**C3. Provenance hashing is broad, and is the reason not to reformat `src/`.**
`src/mp_element_pair.jl` and `src/mp_system_holdout.jl` read and hash roughly ten
`src/*.jl` files, four scripts, two documents and `Project.toml` into
`implementation_hashes`. Any byte change to any of them changes recorded hashes.
The `.gitattributes` `text eol=lf` entries are checkout normalisation, not a
formatting guard. `src/ranking.jl` is in no list, which is why Task 1 was cheap.

**C4. Source paths under `src/` are stable by contract**, enforced by the
provenance-path test in `test/test_mp_element_pair.jl`.

**C5. The v1 command-line surface is frozen** — six subcommands plus the default
bare-query mode.

**C6. No real snapshots, record-level results or credentials enter the
repository**, enforced by `scripts/verify_release.py`.

**C7. Further release-gate rules.** `verify_release.py` rejects `Manifest.toml`
and `.env` by name at any depth, rejects any tracked file containing an absolute
home-directory path, and caps files at 2 MB. Documentation examples therefore use
relative or placeholder paths only.

## Task 1 — Public API contract (complete)

Delivered in `docs/api-stability.md` and `test/test_api.jl`: three tiers (stable,
stable command-line behaviour, experimental), database-schema and
report-format compatibility, and docstrings for the last three undocumented
exports. The provenance-path guard was extended to the `mp_system_holdout` and
`mp_label_sensitivity` lists.

## Task 2 — Package-quality automation, excluding formatting

**Aqua.jl.** Method ambiguities and unbound type parameters are already clean,
and there is no type piracy. Two prerequisites: `Random` and `Test` in
`[extras]` have no `[compat]` entries and Aqua's dependency-compat check
inspects extras, so those and `Aqua` itself need entries. Aqua's undocumented
names check relies on a Julia 1.11+ facility, so it is inert on the 1.10 job;
Task 1 having documented every export removes that asymmetry as a concern.
Adding Aqua to `Project.toml` changes recorded implementation hashes under C3.

**Coverage.** `julia-actions/julia-runtest` already collects coverage; only
processing and upload need adding, on the Ubuntu current-Julia job. A badge
follows the first real measurement, not the configuration.

**Python 3.12 and 3.13.** The four analysis test files run in the Julia `test`
job, not the exporter job, so both jobs need the version matrix or neither gains
coverage. Analysis scripts are standard-library only; the pinned `mp-api` client
is optional and not installed in continuous integration.

**Dependency automation.** Dependabot for GitHub Actions, weekly. CompatHelper
for Julia bounds. `Manifest.toml` is ignored, so there is no lockfile churn. No
pip ecosystem entry: `scripts/requirements-mp.txt` is a deliberately pinned
optional client.

## Task 3 — CONTRIBUTING.md

Setup, the three test commands, the release-gate order, and the repository's
distinctive rules: protocol documents are frozen (C1); provenance paths are
stable (C2–C4); a software fix keeps the protocol identifier while a new
scientific question needs a prospective protocol written before any run; the API
tiers from Task 1; no real data (C6); do not reformat `src/` (C3); no absolute
home paths in examples (C7).

## Task 4 — Documenter site (complete)

Delivered in `docs/make.jl`, `docs/Project.toml` and `docs/src/`, with a
`Documentation` job in `ci.yml` running `julia-actions/julia-docdeploy`.

**The canonical documents are never written back to.** `make.jl` assembles a
staging tree under `docs/staging/` — gitignored, rebuilt from scratch each run —
and Documenter reads that, not `docs/`. All 27 canonical documents are copied
byte for byte, satisfying C1 and leaving C2's manifest keys untouched.

**Layout.** The staging tree mirrors the repository, with `docs/` renamed to
`reference/`: authored pages sit at the root, canonical documents under
`reference/`, and `LICENSE` and `THIRD_PARTY_NOTICES.md` are mirrored from the
repository root. That placement is what makes the `../LICENSE` and
`../THIRD_PARTY_NOTICES.md` links in `mp-data-provenance-review.md`,
`performance.md` and `publication-permissions.md` resolve without editing them.
Documenter rewrites the depth correctly under `prettyurls`, which was verified.
The one build-time transform is on the mirrored `THIRD_PARTY_NOTICES.md`, whose
`docs/...` links become `reference/...`; canonical documents are not rewritten.

**`checkdocs = :exports`.** The manual is required to cover the entire exported
surface, which `docs/src/api.md` does, grouped by the three tiers from Task 1 —
so the API contract and the reference cannot drift apart. The `Research` modules
are listed in `checkdocs_ignored_modules`: they are internal by contract and are
deliberately absent from the site.

**Navigation** is grouped explicitly in `make.jl`. A document that is added to
`docs/` without being grouped still ships, under "Additional documents", and a
group entry naming a document that does not exist fails the build.

**Executable examples.** Five `@example` blocks in `docs/src/getting-started.md`
execute at build time against the shipped fixture, reached through
`pkgdir(EkaCompositions)` rather than a relative path. As anticipated, this
guarantees the examples still run, not that command-line output still matches;
the quick-start shell output remains an unchecked `text` block.

**Deployment.** `deploydocs` publishes to `gh-pages` using `GITHUB_TOKEN`, with
`push_preview` on. GitHub Pages must be pointed at the `gh-pages` branch once,
in repository settings, before the site is reachable. `/dev/` follows `main`;
`/stable/` appears at the next tag, since `v0.1.0` predates this task. The README
carries a dev-documentation badge.

`docs/build/` and `docs/staging/` are ignored, and `docs/Manifest.toml` is
already covered by the repository-wide `Manifest.toml` rule (C7), verified
against the release gate.

## Task 5 — Formatting (deferred to a version boundary)

No blanket reformat. Either check formatting on changed files only, or take a
single whole-repository pass at 0.2.0 with the hash churn under C3 recorded in
the changelog.

## Task 6 — Release checklist (complete)

Delivered in `docs/release-readiness.md`: an ordered pre-tag checklist freezes
and records the candidate commit, runs the Julia, Python and exact-commit archive
gates, requires the matching continuous-integration run and documentation site,
and verifies the commit again immediately before tagging. The 6 September 2026
review records the actual local and CI findings. No tag or release was created.

## Order

1 → 2 → 3 → 4 → 6, with 5 deferred. Each task is a separate commit.
