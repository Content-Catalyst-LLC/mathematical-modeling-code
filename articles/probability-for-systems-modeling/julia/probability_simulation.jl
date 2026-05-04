# Probability for Systems Modeling in Julia
# Monte Carlo estimate for uncertain system loss.
# Educational example only.

using Random
using Statistics

Random.seed!(42)

n = 10000

exposure = rand(n) .* 0.8 .+ 0.2
vulnerability = rand(n) .* 0.8
shock = exp.(randn(n) .* 0.35)

loss = exposure .* vulnerability .* shock

println("Expected loss: ", mean(loss))
println("Median loss: ", median(loss))
println("P95 loss: ", quantile(loss, 0.95))
