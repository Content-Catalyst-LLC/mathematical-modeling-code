rate_function(t, y, decay_rate) = -decay_rate * y
exact_solution(t, y0, decay_rate) = y0 * exp(-decay_rate * t)

function rk4_step(t, y, h, decay_rate)
    k1 = rate_function(t, y, decay_rate)
    k2 = rate_function(t + h / 2, y + h * k1 / 2, decay_rate)
    k3 = rate_function(t + h / 2, y + h * k2 / 2, decay_rate)
    k4 = rate_function(t + h, y + h * k3, decay_rate)
    y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
end

function simulate_rk4(y0, decay_rate, h, stop_time)
    steps = Int(round(stop_time / h))
    y = y0
    for step in 0:(steps - 1)
        t = step * h
        y = rk4_step(t, y, h, decay_rate)
    end
    y
end

y0 = 100.0
decay_rate = 0.35
stop_time = 20.0
exact_final = exact_solution(stop_time, y0, decay_rate)
step_sizes = [1.0, 0.5, 0.25, 0.125]

println("step_size,steps,solver_method,final_numeric_value,final_exact_value,final_absolute_error,warning")
for h in step_sizes
    numeric = simulate_rk4(y0, decay_rate, h, stop_time)
    err = abs(numeric - exact_final)
    println(join((h, Int(round(stop_time / h)), "fixed_step_rk4", numeric, exact_final, err, "Convergence evidence supports numerical reliability not empirical validity."), ","))
end
