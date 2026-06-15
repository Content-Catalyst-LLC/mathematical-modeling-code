population(t) = 100.0 * exp(0.01 * t)
population_rate(t) = 0.01 * population(t)
affluence(t) = 2.0 * exp(0.02 * t)
affluence_rate(t) = 0.02 * affluence(t)

println("rule,model_structure,t,derivative_value,component_a,component_b,warning")
for t in [0.0, 5.0, 10.0, 20.0]
    a = population_rate(t) * affluence(t)
    b = population(t) * affluence_rate(t)
    println("product_rule,impact = population * affluence,$t,$(a+b),$a,$b,")
end
