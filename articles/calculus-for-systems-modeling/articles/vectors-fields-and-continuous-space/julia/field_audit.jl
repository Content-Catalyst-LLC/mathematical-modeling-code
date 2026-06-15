scalar_field(x, y) = 20.0 + 2.0 * sin(x) + 0.5 * y * y
vector_field(x, y) = (-y, x)
vector_magnitude(vx, vy) = sqrt(vx*vx + vy*vy)

function audit_field(step, scenario)
    xs = collect(-3.0:step:3.0)
    ys = collect(-3.0:step:3.0)
    scalars = Float64[]
    magnitudes = Float64[]

    for x in xs
        for y in ys
            push!(scalars, scalar_field(x, y))
            vx, vy = vector_field(x, y)
            push!(magnitudes, vector_magnitude(vx, vy))
        end
    end

    warning = step > 0.75 ? "Grid resolution is coarse; field structure may be undersampled." : "Synthetic field audit; document domain, units, and interpolation assumptions."
    return scenario, step, length(scalars), mean(scalars), minimum(scalars), maximum(scalars), mean(magnitudes), maximum(magnitudes), "square domain [-3,3] x [-3,3]", warning
end

println("scenario,grid_step,point_count,scalar_average,scalar_minimum,scalar_maximum,vector_magnitude_average,vector_magnitude_maximum,domain_description,warning")
for case in [(1.0, "coarse_grid"), (0.5, "medium_grid"), (0.25, "fine_grid")]
    println(join(audit_field(case[1], case[2]), ","))
end
