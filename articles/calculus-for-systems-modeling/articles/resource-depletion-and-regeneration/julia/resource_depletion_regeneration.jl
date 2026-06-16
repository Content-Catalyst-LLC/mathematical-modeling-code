logistic_regeneration(stock, r, k) = max(0.0, r * stock * (1 - stock / k))

function simulate_resource(stock0, harvest, dt, steps)
    stock = stock0
    cumulative = 0.0
    for _ in 1:steps
        extraction = min(stock, harvest * dt)
        growth = logistic_regeneration(stock, 0.18, 1000.0) * dt
        stock = max(0.0, stock + growth - extraction)
        cumulative += extraction
    end
    return stock, cumulative
end

println("scenario_name,resource_type,final_stock,cumulative_extraction,warning")
baseline = simulate_resource(600.0, 35.0, 0.1, 800)
high = simulate_resource(600.0, 60.0, 0.1, 800)
println("renewable_precautionary_harvest,renewable_logistic,$(baseline[1]),$(baseline[2]),precautionary harvest")
println("renewable_high_harvest,renewable_logistic,$(high[1]),$(high[2]),higher harvest pressure")
