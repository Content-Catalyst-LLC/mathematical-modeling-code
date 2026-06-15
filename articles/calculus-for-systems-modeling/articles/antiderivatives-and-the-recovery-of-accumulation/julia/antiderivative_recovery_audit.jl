net_flow(t) = (12.0 + 0.5*t) - (7.0 + 0.2*t)

function recover_stock(times, initial_stock)
    stock = initial_stock
    println("time,net_flow,recovered_stock,method,warning")
    println("$(times[1]),$(net_flow(times[1])),$stock,initial condition,baseline determines recovered level")
    for i in 2:length(times)
        previous = times[i-1]
        current = times[i]
        dt = current - previous
        if dt <= 0
            error("Times must be strictly increasing.")
        end
        area = 0.5 * (net_flow(previous) + net_flow(current)) * dt
        stock += area
        warning = dt > 2 ? "large time step; accumulation may be coarse" : ""
        println("$current,$(net_flow(current)),$stock,trapezoidal accumulation,$warning")
    end
end

recover_stock(0.0:1.0:6.0, 100.0)
