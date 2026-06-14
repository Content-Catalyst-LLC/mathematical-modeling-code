# Julia workflow for mathematical modeling in science.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct PopulationScenario
    key::String
    growth_rate::Float64
    carrying_capacity::Float64
    initial_population::Float64
    years::Int
end

function scenarios()
    [
        PopulationScenario("baseline", 0.28, 500.0, 40.0, 20),
        PopulationScenario("lower_growth", 0.18, 500.0, 40.0, 20),
        PopulationScenario("higher_growth", 0.38, 500.0, 40.0, 20),
        PopulationScenario("lower_capacity", 0.28, 350.0, 40.0, 20),
        PopulationScenario("higher_capacity", 0.28, 700.0, 40.0, 20)
    ]
end

function logistic_final(s)
    population = s.initial_population
    for _ in 1:s.years
        population = population + s.growth_rate * population * (1.0 - population / s.carrying_capacity)
    end
    return population
end

function main()
    items = scenarios()
    finals = [logistic_final(s) for s in items]

    println("key,growth_rate,carrying_capacity,initial_population,years,final_population,crosses_capacity_midpoint")
    for (s, final_value) in zip(items, finals)
        crosses = final_value >= s.carrying_capacity / 2.0
        @printf("%s,%.3f,%.3f,%.3f,%d,%.6f,%s\n",
                s.key, s.growth_rate, s.carrying_capacity, s.initial_population, s.years, final_value, string(crosses))
    end

    @printf("summary,mean_final=%.6f,min_final=%.6f,max_final=%.6f,scenario_spread=%.6f\n",
            mean(finals), minimum(finals), maximum(finals), maximum(finals) - minimum(finals))
end

main()
