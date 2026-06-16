rate_function(t, y, decay_rate) = -decay_rate * y
exact_solution(t, y0, decay_rate) = y0 * exp(-decay_rate * t)

function rk4_step(t, y, h, decay_rate)
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h / 2, y + h * k1 / 2, decay_rate)
    k3 = rate_function(t + h / 2, y + h * k2 / 2, decay_rate)
    k4 = rate_function(t + h, y + h * k3, decay_rate)
    y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
end

y0 = 100.0
decay_rate = 0.35
step_size = 0.5
stop_time = 20.0
steps = Int(round(stop_time / step_size))
y = y0

println("step,time,solver_value,exact_value,absolute_error,solver_method,step_size,warning")
for step in 0:steps
    t = step * step_size
    exact = exact_solution(t, y0, decay_rate)
    println(join((step, t, y, exact, abs(y - exact), "fixed_step_rk4", step_size, "ODE solver outputs depend on equation initial condition method tolerances step size stiffness and diagnostics."), ","))
    global y = rk4_step(t, y, step_size, decay_rate)
end
