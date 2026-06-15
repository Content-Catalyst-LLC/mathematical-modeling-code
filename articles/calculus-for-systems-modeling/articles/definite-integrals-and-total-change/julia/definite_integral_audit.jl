net_rate(t) = 4.0 * sin(t / 2.0) + 1.0

function trapezoid_integral(values, times)
    total = 0.0
    for i in 1:(length(times)-1)
        dt = times[i+1] - times[i]
        if dt <= 0
            error("Times must be strictly increasing.")
        end
        total += 0.5 * (values[i] + values[i+1]) * dt
    end
    return total
end

times = collect(0.0:0.5:4.0)
rates = [net_rate(t) for t in times]
signed_accumulation = trapezoid_integral(rates, times)
absolute_accumulation = trapezoid_integral(abs.(rates), times)

println("interval_start,interval_end,method,signed_accumulation,absolute_accumulation,warning")
println("$(first(times)),$(last(times)),trapezoidal approximation,$signed_accumulation,$absolute_accumulation,signed and absolute accumulation separated")
