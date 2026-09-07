# Post-hoc stability entry point. This deliberately exposes one declared
# sensitivity only: the frozen rank-four fit with its iteration cap raised from
# 2,000 to 20,000. It is not a general tuning or sweep interface.
using EkaCompositions
const MPElementPair = EkaCompositions.Research.MPElementPair
const ElementPairModel = EkaCompositions.Research.ElementPairModel

function main(args)
    synthetic=length(args)==5 && last(args)=="--synthetic"
    length(args)==(synthetic ? 5 : 4)||error(
        "usage: run_element_pair_stability.jl SNAPSHOT AUDIT V2_RESULTS NEW_OUTPUT [--synthetic]")
    settings=ElementPairModel.Settings(max_iterations=20000)
    result=MPElementPair.run_evaluation(args[1:4]...;synthetic,settings,
        analysis_mode="posthoc_stability_20000")
    println("Element-pair stability evaluation: $(length(result.metrics)) metric rows; output: $(result.path)")
end
main(ARGS)
