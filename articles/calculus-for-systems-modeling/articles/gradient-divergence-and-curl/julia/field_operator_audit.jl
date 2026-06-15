scalar_field(x, y) = x*x + y*y
vector_field(x, y) = (-y, x)
gradient_field(x, y) = (2.0*x, 2.0*y)
divergence_field(x, y) = 0.0
curl_2d(x, y) = 2.0
vec_norm(v) = sqrt(v[1]^2 + v[2]^2)
grid_values(step) = collect(-1.0:step:1.0)

function audit_field_operators(step, scenario)
    values = grid_values(step)
    grad_magnitudes = Float64[]
    divergences = Float64[]
    curls = Float64[]

    for x in values
        for y in values
            push!(grad_magnitudes, vec_norm(gradient_field(x,y)))
            push!(divergences, divergence_field(x,y))
            push!(curls, curl_2d(x,y))
        end
    end

    warning = step > 0.5 ? "Grid step is coarse; local derivative structure may be undersampled." : "Synthetic field-operator audit; document field definitions, units, grid, and boundary rules."
    return scenario, step, length(values)^2, sum(grad_magnitudes)/length(grad_magnitudes), maximum(grad_magnitudes), sum(divergences)/length(divergences), sum(curls)/length(curls), maximum(abs.(curls)), "scalar f=x^2+y^2; vector F=<-y,x>", warning
end

println("scenario,grid_step,point_count,mean_gradient_magnitude,maximum_gradient_magnitude,mean_divergence,mean_curl,maximum_abs_curl,field_description,warning")
for case in [(1.0,"coarse_grid"),(0.5,"medium_grid"),(0.25,"fine_grid")]
    println(join(audit_field_operators(case[1], case[2]), ","))
end
