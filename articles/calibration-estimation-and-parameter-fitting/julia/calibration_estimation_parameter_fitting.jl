# Julia workflow for calibration, estimation, and parameter fitting.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct Observation
    time::Int
    stock::Float64
    extraction::Float64
end

struct Candidate
    growth_rate::Float64
    carrying_capacity::Float64
end

function observations()
    [
        Observation(0, 70.0, 5.5),
        Observation(1, 72.8, 5.8),
        Observation(2, 74.1, 6.2),
        Observation(3, 75.0, 6.4),
        Observation(4, 75.5, 6.8),
        Observation(5, 75.2, 7.0),
        Observation(6, 74.7, 7.1),
        Observation(7, 73.8, 7.4),
        Observation(8, 72.6, 7.6),
        Observation(9, 71.2, 7.8)
    ]
end

function score(candidate::Candidate, data)
    stock = data[1].stock
    residuals = Float64[]

    for i in eachindex(data)
        if i == 1
            predicted = stock
        else
            previous = data[i - 1]
            growth = candidate.growth_rate * stock * (1.0 - stock / candidate.carrying_capacity)
            predicted = max(0.0, stock + growth - previous.extraction)
            stock = predicted
        end
        push!(residuals, data[i].stock - predicted)
    end

    sse = sum(r * r for r in residuals)
    return sse, sqrt(sse / length(residuals)), mean(residuals)
end

function main()
    data = observations()
    best_candidate = nothing
    best_sse = Inf
    best_rmse = Inf
    best_bias = 0.0

    for g in 0.08:0.01:0.26
        for k in 85.0:5.0:125.0
            candidate = Candidate(g, k)
            sse, rmse, bias = score(candidate, data)
            if sse < best_sse
                best_sse = sse
                best_rmse = rmse
                best_bias = bias
                best_candidate = candidate
            end
        end
    end

    @printf("best_growth_rate=%.4f best_carrying_capacity=%.4f sse=%.4f rmse=%.4f bias=%.4f\n",
            best_candidate.growth_rate, best_candidate.carrying_capacity, best_sse, best_rmse, best_bias)
end

main()
