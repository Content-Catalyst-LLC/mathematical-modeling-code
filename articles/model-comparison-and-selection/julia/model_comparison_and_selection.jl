# Julia workflow for model comparison and selection.
# Dependency-light: Base + standard libraries only.

using Printf

struct Candidate
    id::String
    family::String
    calibration_rmse::Float64
    validation_rmse::Float64
    parameter_count::Int
    interpretability::Float64
    robustness::Float64
    decision_relevance::Float64
end

function candidates()
    [
        Candidate("baseline_naive", "baseline", 2.90, 3.05, 0, 0.95, 0.72, 0.55),
        Candidate("linear_trend", "statistical", 1.80, 2.10, 2, 0.88, 0.70, 0.68),
        Candidate("logistic_growth", "mechanistic", 1.25, 1.42, 3, 0.76, 0.82, 0.86),
        Candidate("stochastic_shock", "stochastic", 1.05, 1.60, 6, 0.58, 0.88, 0.90),
        Candidate("high_flex_curve", "flexible", 0.45, 2.75, 9, 0.35, 0.40, 0.52)
    ]
end

function score(model::Candidate)
    return model.validation_rmse +
           0.08 * model.parameter_count -
           0.35 * model.interpretability -
           0.40 * model.robustness -
           0.35 * model.decision_relevance
end

function main()
    models = candidates()
    ranked = sort(models, by = score)
    selected = ranked[1]

    println("model_id,comparison_score,overfit_gap")
    for model in ranked
        @printf("%s,%.6f,%.6f\n", model.id, score(model), model.validation_rmse - model.calibration_rmse)
    end

    @printf("selected_model=%s family=%s\n", selected.id, selected.family)
end

main()
