continuous_future_value(v0, r, t) = v0 * exp(r * t)
continuous_present_value(fv, r, t) = fv * exp(-r * t)
discrete_compound_value(v0, r, n, t) = v0 * (1 + r / n)^(n * t)
real_rate(nominal_rate, inflation_rate) = (1 + nominal_rate) / (1 + inflation_rate) - 1

println("scenario_name,model_type,final_value,present_value,warning")
println("continuous_compounding_case,future_value,$(continuous_future_value(1000.0,0.05,30.0)),1000.0,continuous compounding")
println("monthly_compounding_case,discrete_compounding,$(discrete_compound_value(1000.0,0.05,12,30.0)),1000.0,discrete compounding")
println("discounted_future_value,present_value,5000.0,$(continuous_present_value(5000.0,0.05,30.0)),discounting")
println("real_return_case,inflation_adjusted_growth,$(continuous_future_value(1000.0,real_rate(0.06,0.025),30.0)),1000.0,real return")
