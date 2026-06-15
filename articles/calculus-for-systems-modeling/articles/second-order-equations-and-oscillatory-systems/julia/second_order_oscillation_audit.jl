forcing_function(t, amplitude=0.0, frequency=1.0) = amplitude * cos(frequency * t)

function acceleration(position, velocity, time, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency)
    force = forcing_function(time, forcing_amplitude, forcing_frequency)
    damping = 2 * damping_ratio * natural_frequency * velocity
    restoring = natural_frequency^2 * position
    force - damping - restoring
end

function simulate_oscillator(scenario, x0, v0, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency, dt, steps)
    x = x0
    v = v0
    rows = []
    for n in 0:steps
        t = n * dt
        a = acceleration(x, v, t, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency)
        push!(rows, (scenario, t, x, v, a, damping_ratio, natural_frequency, forcing_function(t, forcing_amplitude, forcing_frequency), "explicit_euler_first_order_system", "Explicit Euler is transparent but can distort oscillatory systems if the step size is too large."))
        v = v + dt * a
        x = x + dt * v
    end
    rows
end

println("scenario,time,position,velocity,acceleration,damping_ratio,natural_frequency,forcing,method,warning")
for row in vcat(
    simulate_oscillator("underdamped_unforced", 1.0, 0.0, 0.2, 1.0, 0.0, 1.0, 0.02, 500),
    simulate_oscillator("forced_near_resonance", 1.0, 0.0, 0.1, 1.0, 0.2, 1.0, 0.02, 500)
)
    println(join(row, ","))
end
