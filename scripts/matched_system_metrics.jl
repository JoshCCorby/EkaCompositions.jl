# Post-hoc cross-check for planning task E1. Applies the experimental
# `recovery_metrics` kernel to saved v2 reference rankings and saved primary
# element-pair rankings. Nothing is refit, re-ranked, re-split or relabelled;
# scripts/analyze_matched_system_metrics.py validates input hashes and compares.
#
# Only the kernel's own source files are loaded, so this check does not depend
# on unrelated work in progress elsewhere in the package.
using SHA

const KERNEL_FILES = ("compositions.jl", "benchmark.jl", "ranking_evaluation.jl")
const SYSTEM_DEFINITION = "chemical_system(c::Composition) = join(species(c), \"-\")"
occursin(SYSTEM_DEFINITION, read(joinpath(@__DIR__, "..", "src", "benchmark.jl"), String)) ||
    error("src/benchmark.jl no longer contains the chemical_system definition used here")

module MetricKernel
include(joinpath(@__DIR__, "..", "src", "compositions.jl"))
eval(Meta.parse(Main.SYSTEM_DEFINITION))
include(joinpath(@__DIR__, "..", "src", "ranking_evaluation.jl"))
end
using .MetricKernel: recovery_metrics

const DESIGNS = ("composition", "system")
const POLICIES = ("original", "exclude_mixed", "unlabel_mixed")
const METHODS = ("random", "popularity", "similarity", "element_pair")
const BUDGETS = [20, 50, 100, 200]
const FIELDS = (:hits, :candidate_count, :relevant_count, :selected_system_count,
    :relevant_system_count, :hit_system_count, :system_recall, :effective_hit_systems,
    :largest_hit_system_fraction, :cutoff_score, :cutoff_tie_size, :cutoff_tie_selected,
    :cutoff_tie_crosses)

function table(path)
    lines = readlines(path)
    header = split(first(lines), '\t')
    return [Dict(zip(header, split(line, '\t'; keepempty=true))) for line in lines[2:end]]
end

cell(value) = value === nothing ? "NA" : string(value)

function main(args)
    length(args) == 3 || error("usage: matched_system_metrics.jl V2_RESULTS PAIR_RESULTS NEW_OUTPUT_TSV")
    v2, pair, output = args
    ispath(output) && error("refusing to overwrite $output")
    records = String[join(("design", "policy", "split_seed", "method", "budget", string.(FIELDS)...), '\t')]
    for design in DESIGNS, policy in POLICIES, seed in 0:19
        folder = "split-" * lpad(seed, 2, '0')
        heldout = [row["composition"] for row in table(joinpath(v2, design, policy, folder, "evaluation", "heldout.tsv"))]
        for method in METHODS
            path = method == "element_pair" ? joinpath(pair, design, policy, folder, "ranking.tsv") :
                joinpath(v2, design, policy, folder, method * ".tsv")
            ranked = table(path)
            scores = method == "random" ? nothing : [parse(Float64, row["score"]) for row in ranked]
            rows = recovery_metrics([row["composition"] for row in ranked], heldout; budgets=BUDGETS, scores)
            for row in rows
                push!(records, join((design, policy, seed, method, row.budget,
                    (cell(getproperty(row, field)) for field in FIELDS)...), '\t'))
            end
        end
    end
    open(output, "w") do io
        foreach(line -> println(io, line), records)
    end
    for file in KERNEL_FILES
        println("src/$file sha256=$(bytes2hex(open(sha256, joinpath(@__DIR__, "..", "src", file))))")
    end
    println("Julia recovery_metrics rows: $(length(records) - 1); output: $output")
end
main(ARGS)
