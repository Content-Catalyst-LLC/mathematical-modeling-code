vector_field(x, y) = (-y, x)
dot_product(a, b) = a[1]*b[1] + a[2]*b[2]

function audit_circle_flow(radius, segments, scenario)
    flux_total = 0.0
    circulation_total = 0.0
    tangent_alignments = Float64[]
    normal_alignments = Float64[]
    for i in 0:(segments-1)
        theta0 = 2*pi*i/segments
        theta1 = 2*pi*(i+1)/segments
        x0, y0 = radius*cos(theta0), radius*sin(theta0)
        x1, y1 = radius*cos(theta1), radius*sin(theta1)
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        segment_length = sqrt(dx^2 + dy^2)
        tangent = (dx/segment_length, dy/segment_length)
        normal = (xm/radius, ym/radius)
        field = vector_field(xm, ym)
        circulation_total += dot_product(field, (dx, dy))
        flux_total += dot_product(field, normal) * segment_length
        push!(tangent_alignments, dot_product(field, tangent))
        push!(normal_alignments, dot_product(field, normal))
    end
    warning = segments < 32 ? "Coarse path sampling; circulation and flux should be checked with more segments." : "Synthetic flow audit; document field meaning, orientation, units, and boundary choice."
    return scenario, segments, flux_total, circulation_total, sum(tangent_alignments)/length(tangent_alignments), sum(normal_alignments)/length(normal_alignments), "rotating field F=<-y,x>", "counterclockwise circle with radius $(radius)", warning
end

println("scenario,segment_count,approximate_flux,approximate_circulation,mean_tangential_alignment,mean_normal_alignment,field_description,geometry_description,warning")
for case in [(1.0,16,"coarse_circle"),(1.0,64,"medium_circle"),(1.0,256,"fine_circle")]
    println(join(audit_circle_flow(case[1], case[2], case[3]), ","))
end
