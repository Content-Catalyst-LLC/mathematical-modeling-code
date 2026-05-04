# Statistics for Systems Modeling in Julia
# Educational example only.

values = [18.4, 36.7, 62.1, 28.9, 64.8, 13.7, 43.5, 29.8, 79.4, 30.2]

mean_value = sum(values) / length(values)
variance_value = sum((x - mean_value)^2 for x in values) / (length(values) - 1)
sd_value = sqrt(variance_value)

println("Mean: ", mean_value)
println("Sample variance: ", variance_value)
println("Sample standard deviation: ", sd_value)
