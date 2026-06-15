resource_stock(t) = 1000.0 * exp(-0.01 * t)
resource_stock_rate(t) = -0.01 * resource_stock(t)
population(t) = 100.0 * exp(0.02 * t)
population_rate(t) = 0.02 * population(t)

println("t,numerator,denominator,ratio,numerator_rate,denominator_rate,numerator_effect,denominator_effect,quotient_derivative,ratio_relative_rate")
for t in [0.0, 5.0, 10.0, 20.0, 40.0]
    f = resource_stock(t)
    g = population(t)
    fp = resource_stock_rate(t)
    gp = population_rate(t)
    ratio = f / g
    ne = fp / g
    de = -(f * gp) / (g^2)
    qd = ne + de
    println("$t,$f,$g,$ratio,$fp,$gp,$ne,$de,$qd,$(qd / ratio)")
end
