# Documentation build.
#
# The canonical documents live in `docs/*.md` and are the project's record of
# what was run and under what protocol. Four of them are content-hash-pinned by
# `recovery_protocol()` and five are literal provenance-manifest keys, so this
# build treats every one of them as read-only: it copies them into a staging
# tree and never writes back. `docs/src/` holds the pages authored for the site
# itself, and nothing else.

using Documenter
using DocumenterMermaid
using EkaCompositions

const REPO_ROOT = normpath(joinpath(@__DIR__, ".."))
const AUTHORED = joinpath(@__DIR__, "src")
const STAGING = joinpath(@__DIR__, "staging")

# Canonical documents are copied under this subdirectory. Their cross-links are
# flat and same-directory, so they keep resolving. The two that escape `docs/`
# — `../LICENSE` and `../THIRD_PARTY_NOTICES.md` — resolve because the staging
# root sits exactly one level above, mirroring the repository layout.
const REFERENCE = "reference"

"""
Assemble the Documenter source tree. Returns the sorted list of canonical
document basenames that were copied in.
"""
function stage!()
    rm(STAGING; force = true, recursive = true)
    mkpath(STAGING)

    for entry in readdir(AUTHORED)
        cp(joinpath(AUTHORED, entry), joinpath(STAGING, entry))
    end

    # Mirror the repository root files that canonical documents link to as `../`.
    # The staging tree reproduces the repository layout with one renaming —
    # `docs/` becomes `reference/` — so links pointing into `docs/` from a
    # mirrored root file are rewritten to match. Only these mirrored copies are
    # rewritten; the canonical documents are copied byte for byte.
    for entry in ("LICENSE", "THIRD_PARTY_NOTICES.md")
        source = joinpath(REPO_ROOT, entry)
        destination = joinpath(STAGING, entry)
        if endswith(entry, ".md")
            write(destination, replace(read(source, String), "](docs/" => "](" * REFERENCE * "/"))
        else
            cp(source, destination)
        end
    end

    mkpath(joinpath(STAGING, REFERENCE))
    documents = sort!(filter(endswith(".md"), readdir(@__DIR__)))
    for document in documents
        cp(joinpath(@__DIR__, document), joinpath(STAGING, REFERENCE, document))
    end
    return documents
end

# Canonical documents grouped for the navigation sidebar. A document that is not
# listed here still ships; it lands under "Additional documents" rather than
# being silently dropped from the site.
const GROUPS = [
    "Using the package" => [
        "design.md",
        "api-stability.md",
        "production-validation.md",
        "benchmarking.md",
        "performance.md",
    ],
    "Frozen protocols" => [
        "mp-recovery-protocol.md",
        "mp-label-sensitivity-protocol.md",
        "mp-system-holdout-protocol.md",
        "mp-element-pair-protocol.md",
    ],
    "Recovery pilot" => [
        "mp-pilot.md",
        "mp-pilot-reproduction.md",
        "mp-recovery-splits.md",
        "mp-pu-evaluation.md",
    ],
    "Experiments" => [
        "mp-label-sensitivity.md",
        "mp-system-holdout.md",
        "mp-element-pair.md",
        "mp-learned-feasibility.md",
        "mp-learned-decision.md",
    ],
    "Findings and planning" => [
        "recovery-findings.md",
        "recovery-roadmap.md",
        "engineering-roadmap.md",
        "audit-hardening-compatibility.md",
    ],
    "Data, licensing and release" => [
        "mp-data-provenance-review.md",
        "mp-external-score-provenance.md",
        "mp-terms-evidence.md",
        "publication-permissions.md",
        "release-readiness.md",
    ],
]

"""
Build the `pages` argument, checking that every grouped document actually exists
and sweeping up anything ungrouped.
"""
function reference_pages(documents)
    known = Set(documents)
    grouped = Set{String}()
    pages = Pair{String,Any}[]

    for (title, members) in GROUPS
        for member in members
            member in known || error("docs/$member is listed in GROUPS but does not exist")
            member in grouped && error("docs/$member is listed in GROUPS twice")
            push!(grouped, member)
        end
        push!(pages, title => [joinpath(REFERENCE, m) for m in members])
    end

    leftover = sort!(collect(setdiff(known, grouped)))
    if !isempty(leftover)
        push!(pages, "Additional documents" => [joinpath(REFERENCE, m) for m in leftover])
    end
    return pages
end

documents = stage!()

makedocs(;
    sitename = "EkaCompositions.jl",
    authors = "Joshua Corbett",
    modules = [EkaCompositions],
    source = "staging",
    build = "build",
    # Every exported name is documented and classified by the API contract, so
    # the manual is required to cover the whole exported surface. The internal
    # `Research` modules are not in `modules`, so they are not checked.
    checkdocs = :exports,
    # The research modules are internal by contract and deliberately absent from
    # the reference; without this they would be reported as undocumented pages.
    checkdocs_ignored_modules = [
        EkaCompositions.Research,
        EkaCompositions.Research.MPLabelSensitivity,
        EkaCompositions.Research.MPSystemHoldout,
        EkaCompositions.Research.ElementPairModel,
        EkaCompositions.Research.MPElementPair,
    ],
    format = Documenter.HTML(;
        canonical = "https://JoshCCorby.github.io/EkaCompositions.jl",
        prettyurls = get(ENV, "CI", "false") == "true",
        edit_link = nothing,
    ),
    pages = [
        "Home" => "index.md",
        "Getting started" => "getting-started.md",
        "API reference" => "api.md",
        reference_pages(documents)...,
        "Third-party notices" => "THIRD_PARTY_NOTICES.md",
    ],
)

deploydocs(;
    repo = "github.com/JoshCCorby/EkaCompositions.jl",
    devbranch = "main",
    push_preview = true,
)
