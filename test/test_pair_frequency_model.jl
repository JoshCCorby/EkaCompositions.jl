using SHA

const PairFrequencyModel = EkaCompositions.Research.PairFrequencyModel
const PF = PairFrequencyModel

@testset "Direct pair-frequency control" begin
    training = ["LiNaO", "Li2NaO", "LiKO", "MgCaO"]
    model = PF.fit(training)
    reversed = PF.fit(reverse(training))

    @test model.counts == reversed.counts
    @test model.training == reversed.training == sort(formula.(Composition.(training)))
    @test model.training_count == 4
    @test model.counts[PF.INDEX["Li"], PF.INDEX["Na"]] == 2
    @test PF.score(model, "Li3NaO2").pair_count == 2
    @test PF.score(model, "Li3NaO2").score == log1p(2) / log1p(4)
    @test PF.score(model, "LiNaO2").score == PF.score(model, "Li2NaO3").score
    @test PF.score(model, "CaLiO2") == (
        score=0.0, coverage="unseen_pair_zero", observed_training_pair=false, pair_count=0)

    candidates = ["LiNaO2", "Li2NaO3", "LiCaO2", "KNaO2"]
    ranked = PF.rank_candidates(model, candidates)
    @test ranked == PF.rank_candidates(model, reverse(candidates))
    @test getproperty.(ranked, :score) == sort(getproperty.(ranked, :score); rev=true)
    @test count(row -> row.score == 0.0, ranked) == 2
    @test all(row -> row.tie_key == bytes2hex(sha256(
        "eka-pu-tie-v1\n20260901\n$(formula(row.composition))")), ranked)

    # A valid held-out chemical system has no training observation, so every
    # stoichiometry from it receives the baseline's exact zero score.
    system_training = ["LiNaO", "LiKO", "MgCaO"]
    heldout_system = ["NaKO", "Na2KO3", "NaK2O4"]
    heldout_model = PF.fit(system_training)
    @test all(row -> row.score == 0.0 && row.coverage == "unseen_pair_zero",
        PF.rank_candidates(heldout_model, heldout_system))

    # Labels are evaluator-owned and cannot influence fitting or ranking.
    before = copy(model.counts)
    order = [row.composition for row in ranked]
    @test only(recovery_metrics(order, [first(order)]; budgets=[1],
        scores=getproperty.(ranked, :score))).hits == 1
    @test only(recovery_metrics(order, [last(order)]; budgets=[1],
        scores=getproperty.(ranked, :score))).hits == 0
    @test model.counts == before && PF.rank_candidates(model, candidates) == ranked

    @test_throws ArgumentError PF.fit(vcat(training, ["O2Li2Na2"]))
    @test_throws ArgumentError PF.fit(String[])
    @test_throws ArgumentError PF.fit(["LiNa"])
    @test_throws ArgumentError PF.rank_candidates(model, ["LiNaO"])
    @test_throws ArgumentError PF.rank_candidates(model, ["LiNaO2", "Li2Na2O4"])
    @test_throws ArgumentError PF.rank_candidates(model, candidates; tie_seed=-1)
    @test_throws ArgumentError PF.score(model, "NaCl")
end
