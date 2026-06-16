rate_function(t, y, decay_rate) = -decay_rate * y
exact_solution(t, y0, decay_rate) = y0 * exp(-decay_rate * t)

function euler_step(t, y, h, decay_rate)
    y + h * rate_function(t, y, decay_rate)
end

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
euler_y = y0
rk_y = y0

println("step,time,euler_value,rk4_value,exact_value,euler_absolute_error,rk4_absolute_error,step_size,warning")
for step in 0:steps
    t = step * step_size
    exact = exact_solution(t, y0, decay_rate)
    println(join((step, t, euler_y, rk_y, exact, abs(euler_y - exact), abs(rk_y - exact), step_size, "Runge-Kutta estimates depend on rate function step size smoothness stiffness and benchmark comparison."), ","))
    global euler_y = euler_step(t, euler_y, step_size, decay_rate)
    global rk_y = rk4_step(t, rk_y, step_size, decay_rate)
end
