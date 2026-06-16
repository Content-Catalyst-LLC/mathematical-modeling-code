logistic_solution(t, x0, growth_rate, carrying_capacity) =
    carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))

final_output(growth_rate, carrying_capacity; x0=10.0, stop_time=20.0) =
    logistic_solution(stop_time, x0, growth_rate, carrying_capacity)

growth_rates = [0.18, 0.25, 0.35, 0.45, 0.55]
carrying_capacities = [80.0, 100.0, 125.0, 150.0]

println("growth_rate,carrying_capacity,initial_value,stop_time,final_value,output_metric,warning")
for r in growth_rates
    for k in carrying_capacities
        println(join((r, k, 10.0, 20.0, final_output(r, k), "final_state_value", "Sweep results depend on tested ranges baseline assumptions and model structure."), ","))
    end
end
