vector_field(x, y, z) = (x, y, z)
divergence(x, y, z) = 3.0

function boundary_flux_unit_cube(grid_steps)
    step = 1.0 / grid_steps
    area = step * step
    total = 0.0
    for i in 0:(grid_steps - 1)
        for j in 0:(grid_steps - 1)
            y = (i + 0.5) * step
            z = (j + 0.5) * step
            fx, fy, fz = vector_field(0.0, y, z)
            total += fx * (-1.0) * area
            fx, fy, fz = vector_field(1.0, y, z)
            total += fx * 1.0 * area

            x = (i + 0.5) * step
            z = (j + 0.5) * step
            fx, fy, fz = vector_field(x, 0.0, z)
            total += fy * (-1.0) * area
            fx, fy, fz = vector_field(x, 1.0, z)
            total += fy * 1.0 * area

            x = (i + 0.5) * step
            y = (j + 0.5) * step
            fx, fy, fz = vector_field(x, y, 0.0)
            total += fz * (-1.0) * area
            fx, fy, fz = vector_field(x, y, 1.0)
            total += fz * 1.0 * area
        end
    end
    total
end

function volume_divergence_unit_cube(grid_steps)
    step = 1.0 / grid_steps
    cell_volume = step^3
    total = 0.0
    for i in 0:(grid_steps-1), j in 0:(grid_steps-1), k in 0:(grid_steps-1)
        total += 3.0 * cell_volume
    end
    total
end

function audit_divergence_theorem(grid_steps, scenario)
    flux = boundary_flux_unit_cube(grid_steps)
    div_integral = volume_divergence_unit_cube(grid_steps)
    warning = grid_steps < 8 ? "Coarse grid; refine before interpreting the boundary-volume comparison." : "Synthetic divergence theorem audit; document field, volume, boundary, normals, units, and numerical method."
    return scenario, grid_steps, flux, div_integral, abs(flux-div_integral), "F=<x,y,z>; divergence = 3", "unit cube [0,1] x [0,1] x [0,1]", "all six cube faces use outward normals", warning
end

println("scenario,grid_steps,boundary_flux,volume_divergence_integral,absolute_gap,field_description,volume_description,normal_note,warning")
for case in [(4,"coarse_audit"),(16,"medium_audit"),(64,"fine_audit")]
    println(join(audit_divergence_theorem(case[1], case[2]), ","))
end
