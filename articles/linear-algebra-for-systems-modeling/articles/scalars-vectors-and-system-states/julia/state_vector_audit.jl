values = [72.0, 68.0, 0.91, 0.96, 125000.0]
component_names = ["road_condition", "bridge_condition", "water_reliability", "power_reliability", "transit_capacity"]
raw_l1 = sum(abs.(values))
raw_l2 = sqrt(sum(values .^ 2))

println("position,component_name,value,warning")
for i in eachindex(values)
    println(join((i, component_names[i], values[i], "Scaling review required before norm or distance interpretation"), ","))
end
println("summary,dimension,$(length(values)),raw_l1,$raw_l1,raw_l2,$raw_l2")
