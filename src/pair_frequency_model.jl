"""Direct observed-pair-frequency control for oxygen-containing ternaries."""
module PairFrequencyModel
using ...EkaCompositions
using SHA

const MODEL_ID = "eka-pair-frequency-v1"
const ELEMENTS = sort!([element for element in EkaCompositions.ELEMENT_SYMBOLS if element != "O"])
const INDEX = Dict(element => index for (index, element) in enumerate(ELEMENTS))
check(ok, message) = ok || throw(ArgumentError(message))

function pair(composition::Composition)
    check(length(composition) == 3 && "O" in species(composition),
        "pair-frequency control requires oxygen-containing ternaries")
    a, b = filter(!=("O"), species(composition))
    return INDEX[a], INDEX[b]
end

struct Model
    counts::Matrix{Int}
    training_count::Int
    training::Vector{String}
end

"""
    fit(training)

Count unordered non-oxygen element pairs in unique training compositions. The
model has no fitted parameters and never consumes candidate labels.
"""
function fit(training)
    compositions = sort!(EkaCompositions.pu_compositions(training, "training"); by=formula)
    counts = zeros(Int, length(ELEMENTS), length(ELEMENTS))
    for composition in compositions
        a, b = pair(composition)
        counts[a, b] += 1
        counts[b, a] += 1
    end
    return Model(counts, length(compositions), formula.(compositions))
end

"""Score a candidate by `log1p(pair_count) / log1p(training_count)`."""
function score(model::Model, composition::Composition)
    a, b = pair(composition)
    count = model.counts[a, b]
    value = log1p(count) / log1p(model.training_count)
    check(isfinite(value) && value >= 0, "invalid pair-frequency score")
    return (score=value, coverage=count > 0 ? "observed_pair" : "unseen_pair_zero",
        observed_training_pair=count > 0, pair_count=count)
end
score(model::Model, formula::AbstractString) = score(model, Composition(formula))

"""
    rank_candidates(model, candidates; tie_seed=20260901)

Rank a disjoint, complete candidate set by direct pair frequency. Stoichiometries
of the same chemical system receive the same score; the declared SHA-256 tie key
then gives a deterministic total order.
"""
function rank_candidates(model::Model, candidates; tie_seed=20260901)
    check(tie_seed isa Integer && !(tie_seed isa Bool) && tie_seed >= 0,
        "invalid tie seed")
    compositions = EkaCompositions.pu_compositions(candidates, "candidates")
    check(isempty(intersect(Set(model.training), Set(formula.(compositions)))),
        "training/candidate composition overlap")
    rows = [(composition=composition, score(model, composition)...,
        tie_key=bytes2hex(sha256("eka-pu-tie-v1\n$tie_seed\n$(formula(composition))")))
        for composition in compositions]
    return sort!(rows; by=row -> (-row.score, row.tie_key, formula(row.composition)))
end

end
