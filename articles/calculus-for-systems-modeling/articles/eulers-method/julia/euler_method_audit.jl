rate_function(t, y, decay_rate) = -decay_rate * y
exact_solution(t, y0, decay_rate) = y0 * exp(-decay_rate * t)

y0 = 100.0
decay_rate = 0.35
step_size = 0.1
stop_time = 20.0
steps = Int(round(stop_time / step_size))
multiplier = 1.0 - step_size * decay_rate
status = abs(multiplier) <= 1.0 ? "stable_for_simple_decay" : "unstable_risk"
y = y0

println("step,time,euler_value,exact_value,absolute_error,step_size,stability_multiplier,stability_status,warning")
for step in 0:steps
    t = step * step_size
    exact = exact_solution(t, y0, decay_rate)
    println(join((step, t, y, exact, abs(y - exact), step_size, multiplier, status, "Euler estimates depend on time step rate function initial condition stability and accumulated error."), ","))
    global y = y + step_size * rate_function(t, y, decay_rate)
end
