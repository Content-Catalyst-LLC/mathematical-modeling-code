rotation_field(x, y) = (-y, x)
expansion_field(x, y) = (x, y)
planar_curl(x, y) = 2.0
planar_divergence(x, y) = 2.0

function square_boundary_points(n)
    points = Tuple{Float64,Float64}[]
    for i in 0:(n-1)
        t = -1 + 2*i/n
        push!(points, (t, -1.0))
    end
    for i in 0:(n-1)
        t = -1 + 2*i/n
        push!(points, (1.0, t))
    end
    for i in 0:(n-1)
        t = 1 - 2*i/n
        push!(points, (t, 1.0))
    end
    for i in 0:(n-1)
        t = 1 - 2*i/n
        push!(points, (-1.0, t))
    end
    push!(points, points[1])
    return points
end

function boundary_circulation_square(n)
    points = square_boundary_points(n)
    total = 0.0
    for i in 1:(length(points)-1)
        x0, y0 = points[i]
        x1, y1 = points[i+1]
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        p, q = rotation_field(xm, ym)
        total += p*dx + q*dy
    end
    total
end

function boundary_flux_square(n)
    points = square_boundary_points(n)
    total = 0.0
    for i in 1:(length(points)-1)
        x0, y0 = points[i]
        x1, y1 = points[i+1]
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        nxds, nyds = dy, -dx
        p, q = expansion_field(xm, ym)
        total += p*nxds + q*nyds
    end
    total
end

function interior_integral(step, fn)
    values = collect(-1.0:step:(1.0-step))
    total = 0.0
    for x in values
        for y in values
            total += fn(x+0.5*step, y+0.5*step)*step*step
        end
    end
    total
end

function audit_greens(segments, step, scenario)
    bc = boundary_circulation_square(segments)
    ic = interior_integral(step, planar_curl)
    bf = boundary_flux_square(segments)
    id = interior_integral(step, planar_divergence)
    warning = (segments < 16 || step > 0.25) ? "Coarse boundary or interior sampling; refine before interpreting the theorem comparison." : "Synthetic Green's theorem audit; document field, region, orientation, units, and numerical method."
    return scenario, segments, step, bc, ic, bf, id, abs(bc-ic), abs(bf-id), "circulation F=<-y,x>; flux G=<x,y>", "positively oriented square [-1,1] x [-1,1]", warning
end

println("scenario,boundary_segments_per_side,interior_grid_step,boundary_circulation,interior_curl_integral,boundary_flux,interior_divergence_integral,circulation_gap,flux_gap,field_description,region_description,warning")
for case in [(8,0.5,"coarse_audit"),(32,0.25,"medium_audit"),(128,0.125,"fine_audit")]
    println(join(audit_greens(case[1], case[2], case[3]), ","))
end
