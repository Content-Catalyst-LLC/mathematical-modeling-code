objective(x, y) = x^2 + 2*y^2
constraint(x, y) = x + y
grad_objective(x, y) = (2*x, 4*y)
grad_constraint(x, y) = (1.0, 1.0)

function solve_budget_constraint(target)
    y = target / 3
    x = 2 * target / 3
    lambda_value = 2 * x
    return x, y, lambda_value
end

println("x,y,objective_value,constraint_value,constraint_target,constraint_residual,lambda_value,gradient_f_x,gradient_f_y,gradient_g_x,gradient_g_y,stationarity_residual_norm,feasible,warning")
for target in [12.0, 18.0, 24.0]
    x, y, lambda_value = solve_budget_constraint(target)
    gfx, gfy = grad_objective(x, y)
    ggx, ggy = grad_constraint(x, y)
    stationarity_x = gfx - lambda_value * ggx
    stationarity_y = gfy - lambda_value * ggy
    stationarity_residual_norm = sqrt(stationarity_x^2 + stationarity_y^2)
    cval = constraint(x, y)
    cres = cval - target
    feasible = abs(cres) <= 1e-9
    warning = feasible && stationarity_residual_norm <= 1e-8 ? "Multiplier interpretation is local and unit-dependent." : "Review feasibility or stationarity."
    println("$x,$y,$(objective(x,y)),$cval,$target,$cres,$lambda_value,$gfx,$gfy,$ggx,$ggy,$stationarity_residual_norm,$feasible,$warning")
end
