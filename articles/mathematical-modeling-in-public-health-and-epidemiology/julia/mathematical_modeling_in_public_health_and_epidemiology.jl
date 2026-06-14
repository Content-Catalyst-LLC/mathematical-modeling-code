# Julia workflow for mathematical modeling in public health and epidemiology.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct EpidemicScenario
    key::String
    scenario_name::String
    population::Float64
    initial_infectious::Float64
    initial_recovered::Float64
    beta::Float64
    gamma::Float64
    days::Int
    hospital_capacity::Float64
    hospitalization_rate::Float64
end

function scenarios()
    [
        EpidemicScenario("baseline", "Baseline transmission", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045),
        EpidemicScenario("moderate_intervention", "Moderate intervention", 100000.0, 120.0, 4000.0, 0.24, 0.12, 120, 850.0, 0.045),
        EpidemicScenario("strong_intervention", "Strong intervention", 100000.0, 120.0, 4000.0, 0.18, 0.12, 120, 850.0, 0.045),
        EpidemicScenario("vaccination_plus_intervention", "Vaccination plus intervention", 100000.0, 120.0, 22000.0, 0.20, 0.12, 120, 850.0, 0.030)
    ]
end

function evaluate(s)
    susceptible = s.population - s.initial_infectious - s.initial_recovered
    infectious = s.initial_infectious
    recovered = s.initial_recovered
    peak_infectious = infectious
    peak_hospital_demand = infectious * s.hospitalization_rate

    for _ in 1:s.days
        new_infections = s.beta * susceptible * infectious / s.population
        new_recoveries = s.gamma * infectious
        susceptible = max(0.0, susceptible - new_infections)
        infectious = max(0.0, infectious + new_infections - new_recoveries)
        recovered = min(s.population, recovered + new_recoveries)
        peak_infectious = max(peak_infectious, infectious)
        peak_hospital_demand = max(peak_hospital_demand, infectious * s.hospitalization_rate)
    end

    return peak_infectious, peak_hospital_demand, s.hospital_capacity - peak_hospital_demand, s.beta / s.gamma
end

function main()
    items = scenarios()
    peaks = Float64[]

    println("key,r0_simple,peak_infectious,peak_hospital_demand,capacity_margin,capacity_breach")
    for s in items
        peak_i, peak_h, margin, r0 = evaluate(s)
        push!(peaks, peak_i)
        capacity_breach = peak_h > s.hospital_capacity
        @printf("%s,%.6f,%.6f,%.6f,%.6f,%s\n",
                s.key, r0, peak_i, peak_h, margin, string(capacity_breach))
    end

    @printf("summary,mean_peak_infectious=%.6f,min_peak_infectious=%.6f,max_peak_infectious=%.6f\n",
            mean(peaks), minimum(peaks), maximum(peaks))
end

main()
