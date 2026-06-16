traffic_flow(density, free_flow_speed, jam_density) = max(0.0, free_flow_speed * density * (1 - density / jam_density))
queue_step(queue, arrival_rate, service_rate, dt) = max(0.0, queue + (arrival_rate - service_rate) * dt)
bpr_travel_time(free_flow_time, volume, capacity; alpha=0.15, beta=4.0) = free_flow_time * (1 + alpha * (volume / capacity)^beta)

function simulate_queue(arrival_rate, service_rate, duration, dt)
    queue = 0.0
    total_delay = 0.0
    steps = Int(duration / dt)
    for _ in 1:steps
        queue = queue_step(queue, arrival_rate, service_rate, dt)
        total_delay += queue * dt
    end
    return queue, total_delay
end

below = simulate_queue(1800.0, 2000.0, 3.0, 0.01)
over = simulate_queue(2300.0, 2000.0, 3.0, 0.01)

println("scenario_name,model_type,final_queue,total_delay,travel_time,warning")
println("below_capacity_corridor,queue_and_bpr,$(below[1]),$(below[2]),$(bpr_travel_time(20.0,1800.0,2000.0)),below capacity")
println("over_capacity_bottleneck,queue_and_bpr,$(over[1]),$(over[2]),$(bpr_travel_time(20.0,2300.0,2000.0)),over capacity")
