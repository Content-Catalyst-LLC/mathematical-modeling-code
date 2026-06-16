linear_decline(e0, years) = [max(0.0, e0 * (1 - y / years)) for y in 0:years]
exponential_decline(e0, rate, years) = [e0 * exp(-rate * y) for y in 0:years]
overshoot_pathway(e0, decline_years, negative_years, removal_rate) = vcat(linear_decline(e0, decline_years), fill(-removal_rate, negative_years))

println("scenario_name,pathway_type,cumulative_emissions,warning")
constant = fill(40.0, 31)
linear = linear_decline(40.0, 30)
expo = exponential_decline(40.0, 0.08, 30)
over = overshoot_pathway(40.0, 30, 20, 5.0)
println("constant_emissions,constant,$(sum(constant)),constant emissions continue accumulation")
println("linear_decline_to_zero,linear_decline,$(sum(linear)),linear decline still accumulates until net zero")
println("exponential_decline,exponential_decline,$(sum(expo)),early reductions reduce cumulative burden")
println("overshoot_with_negative_emissions,overshoot,$(sum(over)),negative emissions require feasibility and permanence review")
