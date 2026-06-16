exact_solution(t, y0, eigenvalue) = y0 * exp(eigenvalue * t)

function explicit_euler(y0, eigenvalue, h, stop_time)
    steps = Int(round(stop_time / h))
    amplification = 1 + h * eigenvalue
    y = y0
    for _ in 1:steps
        y = amplification * y
    end
    return y, abs(amplification)
end

function implicit_euler(y0, eigenvalue, h, stop_time)
    steps = Int(round(stop_time / h))
    amplification = 1 / (1 - h * eigenvalue)
    y = y0
    for _ in 1:steps
        y = amplification * y
    end
    return y, abs(amplification)
end

y0 = 1.0
eigenvalue = -50.0
stop_time = 1.0
exact_final = exact_solution(stop_time, y0, eigenvalue)
step_sizes = [0.1, 0.05, 0.025, 0.01]

println("step_size,eigenvalue,method,amplification_factor,stability_status,final_value,exact_final_value,absolute_error,warning")
for h in step_sizes
    ev, ea = explicit_euler(y0, eigenvalue, h, stop_time)
    iv, ia = implicit_euler(y0, eigenvalue, h, stop_time)
    println(join((h, eigenvalue, "explicit_euler", ea, ea <= 1 ? "stable_for_test_problem" : "unstable_for_test_problem", ev, exact_final, abs(ev - exact_final), "Explicit methods may require very small steps on stiff systems."), ","))
    println(join((h, eigenvalue, "implicit_euler", ia, ia <= 1 ? "stable_for_test_problem" : "unstable_for_test_problem", iv, exact_final, abs(iv - exact_final), "Implicit stability does not remove accuracy review."), ","))
end
