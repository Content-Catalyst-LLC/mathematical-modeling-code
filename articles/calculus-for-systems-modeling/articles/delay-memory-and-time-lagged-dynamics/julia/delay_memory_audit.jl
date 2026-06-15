history_function(time, initial_value) = initial_value

function delayed_lookup(states, step, delay_steps, initial_value)
    delayed_index = step - delay_steps
    if delayed_index < 1
        return history_function(0.0, initial_value)
    end
    return states[delayed_index]
end

initial_state = 80.0
target = 100.0
adjustment_rate = 0.2
delay_time = 5.0
dt = 0.1
steps = 300
delay_steps_value = round(Int, delay_time / dt)
states = [initial_state]

println("step,time,current_state,delayed_state,derivative_value,target,absolute_gap,warning")
for step in 0:steps
    time = step * dt
    current_state = states[end]
    delayed_state = delayed_lookup(states, step + 1, delay_steps_value, initial_state)
    derivative_value = adjustment_rate * (target - delayed_state)
    gap = abs(current_state - target)
    println(join((step, time, current_state, delayed_state, derivative_value, target, gap, "Delayed adjustment depends on delay length history function time step and feedback strength."), ","))
    push!(states, current_state + dt * derivative_value)
end
