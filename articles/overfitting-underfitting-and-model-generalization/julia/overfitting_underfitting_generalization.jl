# Julia workflow for overfitting, underfitting, and model generalization.
# Dependency-light: Base + standard libraries only.

using Printf

struct Candidate
    id::String
    family::String
    training_rmse::Float64
    validation_rmse::Float64
    parameter_count::Int
    complexity::Float64
    interpretability::Float64
end

function candidates()
    [
        Candidate("constant_baseline", "baseline", 3.40, 3.55, 0, 0.05, 0.95),
        Candidate("linear_trend", "statistical", 1.95, 2.10, 2, 0.25, 0.88),
        Candidate("logistic_growth", "mechanistic", 1.20, 1.38, 3, 0.45, 0.78),
        Candidate("regularized_curve", "regularized", 0.95, 1.44, 5, 0.62, 0.66),
        Candidate("high_flex_curve", "flexible", 0.28, 2.85, 10, 0.95, 0.30)
    ]
end

function classify(model::Candidate)
    gap = model.validation_rmse - model.training_rmse
    if model.training_rmse >= 3.0 && model.validation_rmse >= 3.0
        return "likely_underfit"
    elseif gap >= 1.0 && model.training_rmse <= 1.0
        return "likely_overfit"
    elseif model.validation_rmse <= 1.5 && gap <= 0.6
        return "generalizes_reasonably"
    else
        return "requires_review"
    end
end

function score(model::Candidate)
    return model.validation_rmse +
           0.20 * model.complexity +
           0.08 * model.parameter_count -
           0.20 * model.interpretability
end

function main()
    models = candidates()
    ranked = sort(models, by = score)
    selected = ranked[1]

    println("model_id,generalization_score,overfit_gap,classification")
    for model in ranked
        @printf("%s,%.6f,%.6f,%s\n", model.id, score(model), model.validation_rmse - model.training_rmse, classify(model))
    end

    @printf("selected_for_review=%s family=%s\n", selected.id, selected.family)
end

main()
