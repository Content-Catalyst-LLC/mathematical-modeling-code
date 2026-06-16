utilization(arrival_rate, capacity) = arrival_rate / capacity
delay_function(u; base_delay=1.0, alpha=0.8) = u >= 1.0 ? Inf : base_delay * (1 + alpha * (u / (1 - u)))

function simulate_queue(arrival_rate, service_capacity, dt, steps)
    queue = 0.0
    max_delay = 0.0
    for _ in 1:steps
        served = min(queue + arrival_rate * dt, service_capacity * dt)
        queue = max(0.0, queue + arrival_rate * dt - served)
        d = delay_function(min(utilization(arrival_rate, service_capacity), 0.999))
        max_delay = max(max_delay, d)
    end
    return queue, utilization(arrival_rate, service_capacity), max_delay
end

println("scenario_name,system_type,final_queue,average_utilization,maximum_delay,warning")
baseline = simulate_queue(75.0, 100.0, 0.1, 240)
near = simulate_queue(95.0, 100.0, 0.1, 240)
over = simulate_queue(115.0, 100.0, 0.1, 240)
println("baseline_spare_capacity,queue_capacity,$(baseline[1]),$(baseline[2]),$(baseline[3]),spare capacity")
println("near_capacity_operation,queue_capacity,$(near[1]),$(near[2]),$(near[3]),near capacity")
println("over_capacity_backlog,queue_capacity,$(over[1]),$(over[2]),$(over[3]),over capacity")
