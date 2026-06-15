restoring_rate(x, equilibrium, recovery_rate) = -recovery_rate * (x - equilibrium)
impulse_shock(time, shock_time, shock_magnitude; tolerance=1e-12) = abs(time - shock_time) < tolerance ? shock_magnitude : 0.0

initial_state = 100.0
equilibrium = 100.0
recovery_rate = 0.15
shock_time = 10.0
shock_magnitude = -30.0
dt = 0.1
steps = 300

baseline = initial_state
forced = initial_state

println("step,time,baseline_state,forced_state,shock_value,absolute_deviation,warning")
for step in 0:steps
    time = step * dt
    shock_value = impulse_shock(time, shock_time, shock_magnitude)
    deviation = abs(forced - baseline)
    println(join((step, time, baseline, forced, shock_value, deviation, "Shock response depends on forcing form timing magnitude recovery rate and numerical step size."), ","))
    global baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate)
    if shock_value != 0.0
        global forced = forced + shock_value
    end
    global forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate)
end
