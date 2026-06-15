height(x, y) = 0.1*x*x + 0.05*y*y
scalar_field(x, y, z) = 1.0 + 0.2*z
vector_field(x, y, z) = (0.1*x, 0.1*y, 1.0)
normal_area_vector(x, y, dx, dy) = (-0.2*x*dx*dy, -0.1*y*dx*dy, dx*dy)
vector_norm(v) = sqrt(v[1]^2 + v[2]^2 + v[3]^2)
dot_product(a, b) = a[1]*b[1] + a[2]*b[2] + a[3]*b[3]

function audit_surface(step, scenario)
    xs = collect(-1.0:step:(1.0-step))
    ys = collect(-1.0:step:(1.0-step))
    surface_area = 0.0
    scalar_total = 0.0
    flux_total = 0.0
    patch_areas = Float64[]
    flux_densities = Float64[]

    for x in xs
        for y in ys
            z = height(x, y)
            area_vector = normal_area_vector(x, y, step, step)
            patch_area = vector_norm(area_vector)
            scalar_value = scalar_field(x, y, z)
            vector_value = vector_field(x, y, z)
            flux = dot_product(vector_value, area_vector)

            surface_area += patch_area
            scalar_total += scalar_value * patch_area
            flux_total += flux
            push!(patch_areas, patch_area)
            push!(flux_densities, flux / max(patch_area, 1.0e-12))
        end
    end

    warning = step > 0.5 ? "Grid step is coarse; curvature and field variation may be undersampled." : "Synthetic surface-integral audit; document surface, normal, units, and mesh."
    return scenario, step, length(patch_areas), surface_area, scalar_total, flux_total, sum(flux_densities)/length(flux_densities), maximum(patch_areas), "graph z = 0.1x^2 + 0.05y^2 over [-1,1] x [-1,1]", warning
end

println("scenario,grid_step,patch_count,approximate_surface_area,scalar_surface_integral,vector_flux_integral,average_flux_density,maximum_patch_area,surface_description,warning")
for case in [(1.0,"coarse_surface_mesh"),(0.5,"medium_surface_mesh"),(0.25,"fine_surface_mesh")]
    println(join(audit_surface(case[1], case[2]), ","))
end
