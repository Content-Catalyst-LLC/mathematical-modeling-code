# Dependency-light Julia continuity and structural-break diagnostics.

piecewise_system(x) = x < 5.0 ? 2.0 + 0.5 * x : 6.0 + 1.4 * (x - 5.0)

xs = collect(0.0:0.25:10.0)
ys = [piecewise_system(x) for x in xs]

println("x,y,left_slope,right_slope,slope_change,level_jump,flag")

for i in eachindex(xs)
    if i == firstindex(xs) || i == lastindex(xs)
        println("$(xs[i]),$(ys[i]),,,,,ok")
    else
        left_slope = (ys[i] - ys[i-1]) / (xs[i] - xs[i-1])
        right_slope = (ys[i+1] - ys[i]) / (xs[i+1] - xs[i])
        slope_change = abs(right_slope - left_slope)
        level_jump = abs(ys[i] - ys[i-1])
        flag = "ok"
        if level_jump > 1.0 && slope_change > 0.5
            flag = "level_and_slope_break"
        elseif level_jump > 1.0
            flag = "possible_jump"
        elseif slope_change > 0.5
            flag = "possible_slope_break"
        end
        println("$(xs[i]),$(ys[i]),$(left_slope),$(right_slope),$(slope_change),$(level_jump),$(flag)")
    end
end
