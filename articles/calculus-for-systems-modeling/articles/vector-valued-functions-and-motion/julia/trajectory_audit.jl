position(t) = (t, sin(t))
distance_between(p, q) = sqrt((q[1]-p[1])^2 + (q[2]-p[2])^2)

function audit_trajectory(step, scenario)
    times = collect(0.0:step:2.0*pi)
    points = [position(t) for t in times]
    segment_lengths = [distance_between(points[i], points[i+1]) for i in 1:(length(points)-1)]
    speeds = [segment_lengths[i] / (times[i+1]-times[i]) for i in 1:length(segment_lengths)]
    arc_length = sum(segment_lengths)
    displacement = distance_between(points[1], points[end])
    efficiency = displacement / max(arc_length, 1.0e-12)
    warning = step > 0.5 ? "Time step is coarse; turns and speed variation may be undersampled." : "Synthetic trajectory audit; document units, parameter meaning, and sampling."
    return scenario, step, length(points), arc_length, displacement, efficiency, sum(speeds)/length(speeds), maximum(speeds), "trajectory r(t) = <t, sin(t)> for 0 <= t <= 2pi", warning
end

println("scenario,time_step,point_count,approximate_arc_length,displacement_magnitude,path_efficiency,average_speed,maximum_speed,domain_description,warning")
for case in [(1.0,"coarse_time_step"),(0.5,"medium_time_step"),(0.25,"fine_time_step")]
    println(join(audit_trajectory(case[1], case[2]), ","))
end
