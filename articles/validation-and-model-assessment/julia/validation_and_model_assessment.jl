# Julia workflow for validation and model assessment.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct ValidationObservation
    time::Int
    observed::Float64
    predicted::Float64
    scenario::String
end

function observations()
    [
        ValidationObservation(10, 70.1, 70.8, "holdout"),
        ValidationObservation(11, 68.9, 69.7, "holdout"),
        ValidationObservation(12, 67.4, 68.3, "holdout"),
        ValidationObservation(13, 65.8, 66.9, "holdout"),
        ValidationObservation(14, 64.2, 65.1, "holdout"),
        ValidationObservation(15, 62.1, 63.8, "stress"),
        ValidationObservation(16, 60.4, 61.3, "stress"),
        ValidationObservation(17, 58.8, 59.9, "stress")
    ]
end

function main()
    data = observations()
    residuals = [item.observed - item.predicted for item in data]
    abs_errors = abs.(residuals)
    squared_errors = residuals .^ 2

    rmse = sqrt(mean(squared_errors))
    mae = mean(abs_errors)
    bias = mean(residuals)
    max_abs_error = maximum(abs_errors)

    fitness = rmse <= 1.25 && max_abs_error <= 2.0 ? "adequate_for_scenario_screening" :
              rmse <= 2.5 ? "limited_use_requires_review" :
              "not_adequate_without_revision"

    @printf("rmse=%.4f mae=%.4f bias=%.4f max_abs_error=%.4f fitness=%s\n",
            rmse, mae, bias, max_abs_error, fitness)
end

main()
