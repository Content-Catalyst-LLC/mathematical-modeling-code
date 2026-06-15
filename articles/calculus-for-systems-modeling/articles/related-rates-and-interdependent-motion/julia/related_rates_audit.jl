volume(h; shape_coefficient=12.0) = shape_coefficient * h^2
d_volume_d_height(h; shape_coefficient=12.0) = 2.0 * shape_coefficient * h
height_path(t) = 2.0 + 0.08 * t
height_rate(t) = 0.08

println("time,height,height_rate,volume,structural_derivative,inferred_volume_rate")
for t in [0.0, 5.0, 10.0, 20.0, 40.0]
    h = height_path(t)
    hr = height_rate(t)
    v = volume(h)
    structural = d_volume_d_height(h)
    inferred = structural * hr
    println("$t,$h,$hr,$v,$structural,$inferred")
end
