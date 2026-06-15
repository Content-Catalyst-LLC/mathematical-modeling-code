path_point(t) = (t, sin(t))
scalar_field(x, y) = 1.0 + y*y
vector_field(x, y) = (1.0, x)
distance_between(p, q) = sqrt((q[1]-p[1])^2 + (q[2]-p[2])^2)
dot_product(a, b) = a[1]*b[1] + a[2]*b[2]

function audit_line_integral(step, scenario)
    times = collect(0.0:step:2.0*pi)
    points = [path_point(t) for t in times]
    path_length = 0.0
    scalar_total = 0.0
    vector_total = 0.0
    alignments = Float64[]
    segment_lengths = Float64[]

    for i in 1:(length(points)-1)
        p = points[i]
        q = points[i+1]
        disp = (q[1]-p[1], q[2]-p[2])
        seg = distance_between(p,q)
        sf = scalar_field(p[1],p[2])
        vf = vector_field(p[1],p[2])
        path_length += seg
        scalar_total += sf * seg
        term = dot_product(vf, disp)
        vector_total += term
        push!(alignments, term / max(seg, 1.0e-12))
        push!(segment_lengths, seg)
    end

    warning = step > 0.5 ? "Time step is coarse; path turns and field variation may be undersampled." : "Synthetic line-integral audit; document path, field, units, and interpolation."
    return scenario, step, length(points), path_length, scalar_total, vector_total, sum(alignments)/length(alignments), maximum(segment_lengths), "path r(t)=<t,sin(t)>", warning
end

println("scenario,time_step,point_count,path_length,scalar_line_integral,vector_line_integral,average_alignment,maximum_segment_length,path_description,warning")
for case in [(1.0,"coarse_path"),(0.5,"medium_path"),(0.25,"fine_path")]
    println(join(audit_line_integral(case[1], case[2]), ","))
end
