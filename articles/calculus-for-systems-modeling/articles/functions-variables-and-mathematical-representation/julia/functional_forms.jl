# Dependency-light Julia functional-form comparison.

linear_model(x; a=10.0, b=2.0) = a + b * x
exponential_model(x; a=10.0, b=0.18) = a * exp(b * x)
logistic_model(x; capacity=100.0, rate=0.75, midpoint=5.0) = capacity / (1.0 + exp(-rate * (x - midpoint)))
threshold_model(x; threshold=5.0, low=20.0, high=80.0) = x < threshold ? low : high

x_values = collect(0.0:0.5:10.0)

println("model,final_value")
println("linear_growth,$(linear_model(last(x_values)))")
println("exponential_growth,$(exponential_model(last(x_values)))")
println("logistic_growth,$(logistic_model(last(x_values)))")
println("threshold_response,$(threshold_model(last(x_values)))")
