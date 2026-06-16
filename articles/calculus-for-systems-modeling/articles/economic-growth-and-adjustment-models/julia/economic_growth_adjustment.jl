exponential_output(y0, g, t) = y0 * exp(g * t)

function logistic_output(y0, r, k, dt, steps)
    y = y0
    for _ in 1:steps
        y = max(0.0, y + r * y * (1 - y / k) * dt)
    end
    return y
end

println("scenario_name,model_type,final_output,warning")
println("constant_growth_projection,exponential_growth,$(exponential_output(100.0,0.025,40.0)),constant proportional growth compounds")
println("capacity_constrained_growth,logistic_constraint,$(logistic_output(100.0,0.06,240.0,0.1,400)),growth slows near capacity")
