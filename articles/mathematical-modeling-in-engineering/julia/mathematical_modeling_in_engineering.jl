# Julia workflow for mathematical modeling in engineering.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct BeamDesign
    key::String
    width_m::Float64
    height_m::Float64
    span_m::Float64
    load_n::Float64
    allowable_stress_pa::Float64
    density::Float64
end

function designs()
    [
        BeamDesign("light_design", 0.08, 0.16, 3.0, 4200.0, 145000000.0, 7850.0),
        BeamDesign("balanced_design", 0.10, 0.18, 3.0, 4200.0, 145000000.0, 7850.0),
        BeamDesign("stiff_design", 0.12, 0.22, 3.0, 4200.0, 145000000.0, 7850.0),
        BeamDesign("overloaded_case", 0.10, 0.18, 3.0, 7000.0, 145000000.0, 7850.0)
    ]
end

function evaluate(design)
    moment = design.load_n * design.span_m / 4.0
    inertia = design.width_m * design.height_m^3 / 12.0
    c_value = design.height_m / 2.0
    stress = moment * c_value / inertia
    margin = design.allowable_stress_pa - stress
    safety_factor = design.allowable_stress_pa / stress
    mass = design.width_m * design.height_m * design.span_m * design.density
    return stress, margin, safety_factor, mass
end

function main()
    items = designs()
    safety_factors = Float64[]

    println("key,width_m,height_m,load_n,max_stress_pa,stress_margin_pa,safety_factor,estimated_mass_kg,passes_stress_constraint")
    for d in items
        stress, margin, safety_factor, mass = evaluate(d)
        push!(safety_factors, safety_factor)
        passes = stress <= d.allowable_stress_pa
        @printf("%s,%.3f,%.3f,%.3f,%.6f,%.6f,%.6f,%.6f,%s\n",
                d.key, d.width_m, d.height_m, d.load_n, stress, margin, safety_factor, mass, string(passes))
    end

    @printf("summary,mean_safety_factor=%.6f,min_safety_factor=%.6f,max_safety_factor=%.6f\n",
            mean(safety_factors), minimum(safety_factors), maximum(safety_factors))
end

main()
