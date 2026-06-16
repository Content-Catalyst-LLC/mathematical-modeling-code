regeneration(stock, growth_rate, carrying_capacity) = growth_rate * stock * (1 - stock / carrying_capacity)
extraction(efficiency, effort, stock) = efficiency * effort * stock
adaptive_effort_step(effort, scarcity, governance, adjustment, dt) = max(0.0, effort - adjustment * governance * scarcity * dt)
natural_stock_step(stock, growth_rate, carrying_capacity, extraction_amount, stress, dt) = max(0.0, stock + (regeneration(stock, growth_rate, carrying_capacity) - extraction_amount - stress) * dt)

function simulate(growth_rate, carrying_capacity, efficiency, effort0, governance, adjustment, stress, stock0, dt, steps)
    stock = stock0
    effort = effort0
    cumulative_extraction = 0.0
    for _ in 1:steps
        scarcity = max(0.0, 1 - stock / carrying_capacity)
        harvest = extraction(efficiency, effort, stock)
        stock = natural_stock_step(stock, growth_rate, carrying_capacity, harvest, stress, dt)
        effort = adaptive_effort_step(effort, scarcity, governance, adjustment, dt)
        cumulative_extraction += harvest * dt
    end
    return effort, stock, cumulative_extraction
end

baseline = simulate(0.08, 100.0, 0.003, 12.0, 0.60, 0.20, 0.25, 80.0, 0.25, 160)
restoration = simulate(0.10, 110.0, 0.0025, 10.0, 0.85, 0.30, 0.15, 80.0, 0.25, 160)

println("scenario_name,model_type,final_human_pressure,final_natural_stock,cumulative_extraction,warning")
println("baseline_coupled_resource,resource_governance_feedback,$(baseline[1]),$(baseline[2]),$(baseline[3]),baseline")
println("restoration_and_adaptation,resource_governance_feedback,$(restoration[1]),$(restoration[2]),$(restoration[3]),restoration")
