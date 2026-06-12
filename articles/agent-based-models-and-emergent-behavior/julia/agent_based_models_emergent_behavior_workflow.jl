# Julia workflow for agent-based models and emergent behavior.
# Dependency-light: Base only.

using Random
using Printf

mutable struct Agent
    threshold::Float64
    adopted::Bool
end

function neighbors(i, n)
    return [mod1(i - 2, n), mod1(i - 1, n), mod1(i + 1, n), mod1(i + 2, n)]
end

function run_adoption(seed, n, initial_adopters, low, high, steps)
    rng = MersenneTwister(seed)
    agents = [Agent(rand(rng) * (high - low) + low, false) for _ in 1:n]

    initial = randperm(rng, n)[1:initial_adopters]
    for idx in initial
        agents[idx].adopted = true
    end

    for _ in 1:steps
        next_state = [agent.adopted for agent in agents]
        for i in 1:n
            if agents[i].adopted
                continue
            end
            adopted_neighbors = sum(agents[j].adopted ? 1 : 0 for j in neighbors(i, n))
            share = adopted_neighbors / 4
            if share >= agents[i].threshold
                next_state[i] = true
            end
        end
        for i in 1:n
            agents[i].adopted = next_state[i]
        end
    end

    return sum(agent.adopted ? 1 : 0 for agent in agents) / n
end

function main()
    scenarios = [
        ("julia_baseline", 0.25, 0.55),
        ("julia_low_threshold", 0.10, 0.35),
        ("julia_high_threshold", 0.45, 0.75)
    ]

    for (name, low, high) in scenarios
        outcomes = [run_adoption(seed, 100, 8, low, high, 30) for seed in 1:40]
        @printf("%s mean_final_adoption=%.4f min=%.4f max=%.4f\n",
                name, sum(outcomes) / length(outcomes), minimum(outcomes), maximum(outcomes))
    end
end

main()
