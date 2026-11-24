@testset "Recovery metrics: composition and system recovery" begin
    ranking = ["LiNaO", "Li2NaO", "CaTiO3", "MgAl2O4"]
    relevant = ["MgAl2O4", "Li2NaO", "LiNaO"]
    scores = [0.9, 0.9, 0.9, 0.1]
    saved_ranking, saved_relevant, saved_scores = copy(ranking), copy(relevant), copy(scores)

    rows = recovery_metrics(ranking, relevant; budgets=[4, 1, 3, 2], scores)
    @test getproperty.(rows, :budget) == [1, 2, 3, 4]
    @test getproperty.(rows, :hits) == [1, 2, 2, 3]
    @test getproperty.(rows, :candidate_count) == fill(4, 4)
    @test getproperty.(rows, :relevant_count) == fill(3, 4)
    @test getproperty.(rows, :observed_label_fraction) == [1.0, 1.0, 2/3, 3/4]
    @test getproperty.(rows, :recall) == [1/3, 2/3, 2/3, 1.0]
    @test getproperty.(rows, :enrichment) == [4/3, 4/3, 8/9, 1.0]
    @test getproperty.(rows, :random_expected_hits) == [3/4, 3/2, 9/4, 3.0]
    @test [(r.random_expected_hits_numerator, r.random_expected_hits_denominator) for r in rows] ==
        [(3, 4), (3, 2), (9, 4), (3, 1)]

    discount2 = inv(log2(3))
    discount3 = inv(log2(4))
    discount4 = inv(log2(5))
    @test getproperty.(rows, :dcg) ≈ [1.0, 1 + discount2, 1 + discount2, 1 + discount2 + discount4]
    @test getproperty.(rows, :ndcg) ≈ [1.0, 1.0,
        (1 + discount2) / (1 + discount2 + discount3),
        (1 + discount2 + discount4) / (1 + discount2 + discount3)]

    @test getproperty.(rows, :selected_system_count) == [1, 1, 2, 3]
    @test getproperty.(rows, :relevant_system_count) == fill(2, 4)
    @test getproperty.(rows, :hit_system_count) == [1, 1, 1, 2]
    @test getproperty.(rows, :system_recall) == [0.5, 0.5, 0.5, 1.0]
    @test getproperty.(rows, :effective_hit_systems) == [1.0, 1.0, 1.0, 1.8]
    @test getproperty.(rows, :largest_hit_system_fraction) == [1.0, 1.0, 1.0, 2/3]

    @test getproperty.(rows, :cutoff_score) == scores
    @test getproperty.(rows, :cutoff_tie_size) == [3, 3, 3, 1]
    @test getproperty.(rows, :cutoff_tie_selected) == [1, 2, 3, 1]
    @test getproperty.(rows, :cutoff_tie_crosses) == [true, true, false, false]
    @test (ranking, relevant, scores) == (saved_ranking, saved_relevant, saved_scores)

    # Canonical formula spellings and relevance order cannot change the result.
    equivalent = recovery_metrics(Composition.(ranking),
        ["O2Na2Li2", "O2Na2Li4", "O4Mg1Al2"]; budgets=[1, 2, 3, 4], scores)
    @test equivalent == rows
end

@testset "Recovery metrics: edge cases and validation" begin
    ranking = ["LiNaO", "CaTiO3", "MgAl2O4", "BaTiO3"]

    no_hit = only(recovery_metrics(ranking, [last(ranking)]; budgets=[1]))
    @test no_hit.hits == 0 && no_hit.recall == 0.0 && no_hit.ndcg == 0.0
    @test no_hit.hit_system_count == 0 && no_hit.effective_hit_systems == 0.0
    @test no_hit.largest_hit_system_fraction == 0.0
    @test no_hit.cutoff_score === nothing && no_hit.cutoff_tie_size === nothing
    @test no_hit.cutoff_tie_selected === nothing && no_hit.cutoff_tie_crosses === nothing

    signed_zero = only(recovery_metrics(ranking, ["LiNaO"]; budgets=[1],
        scores=[0.0, -0.0, -1.0, -2.0]))
    @test signed_zero.cutoff_tie_size == 2
    @test signed_zero.cutoff_tie_selected == 1
    @test signed_zero.cutoff_tie_crosses === true

    all_relevant = recovery_metrics(ranking, ranking; budgets=[1, 4])
    @test getproperty.(all_relevant, :hits) == [1, 4]
    @test getproperty.(all_relevant, :recall) == [0.25, 1.0]
    @test getproperty.(all_relevant, :ndcg) == [1.0, 1.0]
    @test last(all_relevant).system_recall == 1.0

    @test_throws ArgumentError recovery_metrics([], ["LiNaO"]; budgets=[1])
    @test_throws ArgumentError recovery_metrics(ranking, []; budgets=[1])
    @test_throws ArgumentError recovery_metrics(ranking, ["SrTiO3"]; budgets=[1])
    @test_throws ArgumentError recovery_metrics(vcat(ranking, ["O2Li2Na2"]), ["LiNaO"]; budgets=[1])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO", "O2Li2Na2"]; budgets=[1])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[0])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[5])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[1, 1])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[true])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets="1")
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[1], scores=[1.0])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[1], scores=[1.0, 0.9, NaN, 0.1])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[1], scores=[1.0, 0.8, 0.9, 0.1])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[1], scores=Any[true, 0.9, 0.8, 0.7])
    @test_throws ArgumentError recovery_metrics(ranking, ["LiNaO"]; budgets=[1], scores="scores")
    @test_throws ArgumentError recovery_metrics([("LiNaO", 1.0)], ["LiNaO"]; budgets=[1])
end
