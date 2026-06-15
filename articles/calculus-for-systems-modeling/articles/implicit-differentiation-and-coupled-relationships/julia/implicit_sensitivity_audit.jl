equilibrium_state(p) = (-p + sqrt(p^2 + 40.0)) / 2.0
constraint(x, p) = x^2 + p*x - 10.0
partial_state(x, p) = 2.0*x + p
partial_parameter(x, p) = x
implicit_sensitivity(x, p) = -partial_parameter(x, p) / partial_state(x, p)

println("parameter,equilibrium_state,constraint_value,partial_state,partial_parameter,implicit_sensitivity")
for p in [-3.0, -1.0, 0.0, 1.0, 3.0]
    x = equilibrium_state(p)
    gx = partial_state(x, p)
    gp = partial_parameter(x, p)
    sens = implicit_sensitivity(x, p)
    println("$p,$x,$(constraint(x,p)),$gx,$gp,$sens")
end
