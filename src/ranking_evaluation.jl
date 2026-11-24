function evaluation_compositions(rows, label)
    rows isa AbstractString && throw(ArgumentError("$label must be a collection"))
    result = Composition[]
    seen = Set{Composition}()
    for row in rows
        row isa Union{Composition,AbstractString} ||
            throw(ArgumentError("$label must contain formulas or Composition values"))
        composition = row isa Composition ? row : Composition(row)
        composition in seen &&
            throw(ArgumentError("duplicate canonical $label composition: $(formula(composition))"))
        push!(seen, composition)
        push!(result, composition)
    end
    isempty(result) && throw(ArgumentError("$label must not be empty"))
    return result
end

function evaluation_budgets(values, candidate_count)
    values isa Union{Integer,AbstractString} &&
        throw(ArgumentError("budgets must be a collection"))
    budgets = Int[]
    for value in values
        value isa Integer && !(value isa Bool) && 1 <= value <= candidate_count ||
            throw(ArgumentError("budgets must contain integers between 1 and the candidate count"))
        push!(budgets, Int(value))
    end
    isempty(budgets) && throw(ArgumentError("budgets must not be empty"))
    length(unique(budgets)) == length(budgets) || throw(ArgumentError("duplicate budgets"))
    return sort!(budgets)
end

function evaluation_scores(values, candidate_count)
    values === nothing && return nothing
    values isa Union{Real,AbstractString} && throw(ArgumentError("scores must be a collection"))
    scores = Float64[]
    for value in values
        value isa Real && !(value isa Bool) && isfinite(value) && isfinite(Float64(value)) ||
            throw(ArgumentError("scores must contain finite real values"))
        push!(scores, Float64(value))
    end
    length(scores) == candidate_count || throw(ArgumentError("scores must align with the complete ranking"))
    issorted(scores; rev=true) || throw(ArgumentError("scores must be in descending ranking order"))
    return scores
end

"""
    recovery_metrics(ranking, relevant; budgets, scores=nothing)

Evaluate a complete ordering of unique canonical compositions against a nonempty
held-out relevant subset. The ranked item is a composition; its chemical system
is the unordered set of its elements. For each budget, return composition hits,
observed-label fraction, recall, enrichment, exact uniform-random expectation,
binary DCG/NDCG, and system-concentration diagnostics.

`scores`, when supplied, must be finite and aligned in descending order. Exact
score equality is used to report the cutoff tie size, how many members of that
tie are selected, and whether the tie crosses the cutoff. No score rounding is
performed. This function evaluates an existing order: it does not rank, filter,
fit, mutate inputs, or interpret unlabelled compositions as confirmed negatives.
Invalid budgets, duplicates, empty relevance, or relevance outside the ranking
are errors.
"""
function recovery_metrics(ranking, relevant; budgets, scores=nothing)
    ranking = evaluation_compositions(ranking, "ranking")
    relevant = evaluation_compositions(relevant, "relevant")
    relevant_set = Set(relevant)
    issubset(relevant_set, Set(ranking)) ||
        throw(ArgumentError("relevant composition absent from ranking"))
    candidate_count = length(ranking)
    relevant_count = length(relevant)
    budgets = evaluation_budgets(budgets, candidate_count)
    scores = evaluation_scores(scores, candidate_count)

    relevant_systems = Set(chemical_system(composition) for composition in relevant)
    selected_systems = Set{String}()
    hit_system_counts = Dict{String,Int}()
    score_frequencies = if scores === nothing
        Dict{Float64,Int}()
    else
        frequencies = Dict{Float64,Int}()
        for score in scores
            key = iszero(score) ? 0.0 : score
            frequencies[key] = get(frequencies, key, 0) + 1
        end
        frequencies
    end

    rows = NamedTuple[]
    hits = 0
    dcg = 0.0
    budget_index = 1
    for (rank, composition) in enumerate(ranking)
        system = chemical_system(composition)
        push!(selected_systems, system)
        if composition in relevant_set
            hits += 1
            dcg += inv(log2(rank + 1))
            hit_system_counts[system] = get(hit_system_counts, system, 0) + 1
        end
        budget_index > length(budgets) && continue
        rank == budgets[budget_index] || continue

        budget = rank
        ideal_dcg = sum(inv(log2(i + 1)) for i in 1:min(budget, relevant_count))
        expected = (big(budget) * relevant_count) // candidate_count
        effective_hit_systems = hits == 0 ? 0.0 :
            Float64(hits)^2 / sum(Float64(count)^2 for count in values(hit_system_counts))
        largest_hit_system_fraction = hits == 0 ? 0.0 :
            maximum(values(hit_system_counts)) / hits
        cutoff_score = scores === nothing ? nothing : scores[budget]
        cutoff_key = cutoff_score === nothing || !iszero(cutoff_score) ? cutoff_score : 0.0
        cutoff_tie_size = scores === nothing ? nothing : score_frequencies[cutoff_key]
        cutoff_tie_selected = scores === nothing ? nothing : count(==(cutoff_score), @view scores[1:budget])
        cutoff_tie_crosses = scores === nothing ? nothing : cutoff_tie_selected < cutoff_tie_size

        push!(rows, (budget=budget, hits=hits, candidate_count=candidate_count,
            relevant_count=relevant_count, observed_label_fraction=hits / budget,
            recall=hits / relevant_count,
            enrichment=(hits / budget) / (relevant_count / candidate_count),
            random_expected_hits=Float64(expected),
            random_expected_hits_numerator=numerator(expected),
            random_expected_hits_denominator=denominator(expected),
            dcg=dcg, ndcg=dcg / ideal_dcg,
            selected_system_count=length(selected_systems),
            relevant_system_count=length(relevant_systems),
            hit_system_count=length(hit_system_counts),
            system_recall=length(hit_system_counts) / length(relevant_systems),
            effective_hit_systems=effective_hit_systems,
            largest_hit_system_fraction=largest_hit_system_fraction,
            cutoff_score=cutoff_score, cutoff_tie_size=cutoff_tie_size,
            cutoff_tie_selected=cutoff_tie_selected,
            cutoff_tie_crosses=cutoff_tie_crosses))
        budget_index += 1
    end
    return rows
end
