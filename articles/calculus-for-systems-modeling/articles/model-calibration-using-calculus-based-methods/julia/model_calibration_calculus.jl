logistic_solution(t, x0, growth_rate, carrying_capacity) =
    carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))

times = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]
observed = [10.0, 17.5, 29.2, 44.1, 60.5, 74.0, 83.2]
growth_rates = [0.22, 0.26, 0.30, 0.34, 0.38, 0.42]
capacities = [85.0, 95.0, 105.0, 115.0, 125.0]

println("growth_rate,carrying_capacity,loss,mean_absolute_residual,max_absolute_residual,warning")
for r in growth_rates
    for k in capacities
        residuals = [observed[i] - logistic_solution(times[i], 10.0, r, k) for i in eachindex(times)]
        sq = residuals .^ 2
        absr = abs.(residuals)
        println(join((r, k, sum(sq), sum(absr) / length(absr), maximum(absr), "Calibration fit does not prove model validity validation and sensitivity review remain required."), ","))
    end
end
