function predator_prey_rates(x, y, alpha, beta, delta, gamma)
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    dxdt, dydt
end

alpha = 0.7
beta = 0.05
delta = 0.02
gamma = 0.5

println("x,y,dxdt,dydt,x_nullcline_residual,y_nullcline_residual,speed,warning")
for x in 0:5:60
    for y in 0:3:30
        dxdt, dydt = predator_prey_rates(Float64(x), Float64(y), alpha, beta, delta, gamma)
        speed = sqrt(dxdt^2 + dydt^2)
        println(join((x, y, dxdt, dydt, dxdt, dydt, speed, "Vector-field values depend on parameter values, state ranges, and the assumed interaction structure."), ","))
    end
end
