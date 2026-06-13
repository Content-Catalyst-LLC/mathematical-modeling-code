# Julia workflow for diagnostics, residuals, and model error.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct Observation
    time::Int
    group::String
    observed::Float64
    predicted::Float64
    threshold::Float64
end

function observations()
    [
        Observation(1, "baseline", 82.0, 81.5, 70.0),
        Observation(2, "baseline", 79.5, 80.2, 70.0),
        Observation(3, "baseline", 77.0, 78.4, 70.0),
        Observation(4, "baseline", 74.3, 75.6, 70.0),
        Observation(5, "threshold", 71.5, 72.8, 70.0),
        Observation(6, "threshold", 69.2, 71.0, 70.0),
        Observation(7, "threshold", 67.8, 69.8, 70.0),
        Observation(8, "stress", 65.5, 68.0, 70.0),
        Observation(9, "stress", 63.0, 66.4, 70.0),
        Observation(10, "stress", 61.1, 65.2, 70.0)
    ]
end

function main()
    data = observations()
    residuals = [item.observed - item.predicted for item in data]
    abs_errors = abs.(residuals)
    rmse = sqrt(mean(residuals .^ 2))
    mae = mean(abs_errors)
    mean_error = mean(residuals)
    max_abs_error = maximum(abs_errors)

    disagreements = sum(((item.observed < item.threshold) != (item.predicted < item.threshold)) for item in data)

    @printf("mean_error=%.4f mae=%.4f rmse=%.4f max_abs_error=%.4f decision_disagreements=%d\n",
            mean_error, mae, rmse, max_abs_error, disagreements)
end

main()
