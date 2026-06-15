exposure_cartesian(x, y) = begin
    r = sqrt(x*x + y*y)
    20.0 * exp(-0.4 * r)
end
exposure_polar(r, theta) = 20.0 * exp(-0.4 * r)

function polar_total(radius, radial_step, angular_step)
    total = 0.0
    r = radial_step / 2.0
    while r < radius
        theta = angular_step / 2.0
        while theta < 2.0*pi
            total += exposure_polar(r, theta) * r * radial_step * angular_step
            theta += angular_step
        end
        r += radial_step
    end
    return total
end

function cartesian_grid_total(radius, step)
    total = 0.0
    n = Int(floor((2.0 * radius) / step))
    for i in 0:n
        x = -radius + i * step
        for j in 0:n
            y = -radius + j * step
            if x*x + y*y <= radius*radius
                total += exposure_cartesian(x, y) * step * step
            end
        end
    end
    return total
end

function audit(radius, radial_step, angular_step, scenario)
    p_total = polar_total(radius, radial_step, angular_step)
    c_total = cartesian_grid_total(radius, radial_step)
    diff = abs(p_total - c_total)
    rel = diff / max(abs(p_total), 1.0e-12)
    warning = radial_step > 0.5 ? "Resolution is coarse; transformed and Cartesian approximations may differ." : "Polar Jacobian factor r included; compare domain and resolution assumptions."
    return scenario, radius, radial_step, angular_step, p_total, c_total, diff, rel, "dA = r dr dtheta", warning
end

println("scenario,radius,radial_step,angular_step,polar_total,cartesian_grid_total,absolute_difference,relative_difference,jacobian_rule,warning")
for case in [(3.0,0.5,pi/24,"medium_polar_grid"),(3.0,0.25,pi/48,"fine_polar_grid"),(3.0,0.125,pi/96,"very_fine_polar_grid")]
    println(join(audit(case[1], case[2], case[3], case[4]), ","))
end
