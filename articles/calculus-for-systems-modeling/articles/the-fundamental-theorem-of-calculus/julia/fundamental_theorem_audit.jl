state(t) = 50.0 + 2.0 * t + 3.0 * sin(t)
rate(t) = 2.0 + 3.0 * cos(t)

function trapezoid_integral(times)
    total = 0.0
    for i in 1:(length(times)-1)
        previous = times[i]
        current = times[i+1]
        dt = current - previous
        if dt <= 0
            error("Times must be strictly increasing.")
        end
        total += 0.5 * (rate(previous) + rate(current)) * dt
    end
    return total
end

times = collect(0.0:0.25:2.0)
state_start = state(first(times))
state_end = state(last(times))
endpoint_difference = state_end - state_start
accumulated_rate = trapezoid_integral(times)
residual = endpoint_difference - accumulated_rate

println("interval_start,interval_end,state_start,state_end,endpoint_difference,accumulated_rate,residual,method")
println("$(first(times)),$(last(times)),$state_start,$state_end,$endpoint_difference,$accumulated_rate,$residual,trapezoidal approximation")
