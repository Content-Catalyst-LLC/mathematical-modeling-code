equilibrium_temperature(forcing, feedback) = forcing / feedback
adjustment_time(heat_capacity, feedback) = heat_capacity / feedback
function one_layer_response(forcing, feedback, heat_capacity, initial_temperature, dt, steps)
    temperature = initial_temperature
    for _ in 1:steps
        imbalance = forcing - feedback * temperature
        temperature += (imbalance / heat_capacity) * dt
    end
    return temperature
end
baseline = one_layer_response(3.7, 1.2, 10.0, 0.0, 0.1, 1500)
stronger = one_layer_response(3.7, 1.8, 10.0, 0.0, 0.1, 1500)
larger_capacity = one_layer_response(3.7, 1.2, 40.0, 0.0, 0.1, 1500)
println("scenario_name,model_type,final_temperature,equilibrium_temperature,adjustment_time,warning")
println("baseline_one_layer,one_layer,$baseline,$(equilibrium_temperature(3.7,1.2)),$(adjustment_time(10.0,1.2)),baseline")
println("stronger_feedback,one_layer,$stronger,$(equilibrium_temperature(3.7,1.8)),$(adjustment_time(10.0,1.8)),stronger feedback")
println("larger_heat_capacity,one_layer,$larger_capacity,$(equilibrium_temperature(3.7,1.2)),$(adjustment_time(40.0,1.2)),larger heat capacity")
