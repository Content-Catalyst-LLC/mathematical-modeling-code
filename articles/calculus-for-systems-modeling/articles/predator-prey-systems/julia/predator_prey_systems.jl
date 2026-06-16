function simulate_pair(x0, y0, derivative, dt, steps)
    x = x0
    y = y0
    for _ in 1:steps
        dx, dy = derivative(x, y)
        x = max(0.0, x + dt * dx)
        y = max(0.0, y + dt * dy)
    end
    return x, y
end

lotka_volterra(alpha, beta, gamma, delta) = (x, y) -> (alpha*x - beta*x*y, delta*x*y - gamma*y)
logistic_prey(r, k, beta, gamma, delta) = (x, y) -> (r*x*(1-x/k) - beta*x*y, delta*x*y - gamma*y)

x0 = 40.0
y0 = 9.0
dt = 0.02
steps = 4000

classic = simulate_pair(x0, y0, lotka_volterra(0.6, 0.02, 0.5, 0.01), dt, steps)
limited = simulate_pair(x0, y0, logistic_prey(0.6, 500.0, 0.02, 0.5, 0.01), dt, steps)

println("scenario_name,model_type,final_prey,final_predator,warning")
println("classic_lotka_volterra,lotka_volterra,$(classic[1]),$(classic[2]),mass-action baseline")
println("logistic_prey_limit,logistic_prey,$(limited[1]),$(limited[2]),prey capacity included")
