equilibrium(input_rate, loss_rate) = input_rate / loss_rate
rate_law(y, input_rate, loss_rate) = input_rate - loss_rate * y
analytical_solution(t, y0, input_rate, loss_rate) = equilibrium(input_rate, loss_rate) + (y0 - equilibrium(input_rate, loss_rate)) * exp(-loss_rate * t)

function simulate_linear_input_loss(y0, input_rate, loss_rate, dt, steps)
    y = y0
    eq = equilibrium(input_rate, loss_rate)
    rows = []
    for n in 0:steps
        t = n * dt
        analytical = analytical_solution(t, y0, input_rate, loss_rate)
        push!(rows, ("input_loss_balance", t, analytical, y, abs(analytical-y), input_rate, loss_rate, eq, y0, "analytical_vs_explicit_euler", "Assumes constant input and proportional loss."))
        y = y + dt * rate_law(y, input_rate, loss_rate)
    end
    rows
end

println("scenario,time,analytical_state,euler_state,absolute_error,input_rate,loss_rate,equilibrium,initial_state,method,warning")
for row in simulate_linear_input_loss(20.0, 12.0, 0.4, 0.1, 100)
    println(join(row, ","))
end
