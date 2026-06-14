# Dependency-light Julia differentiability diagnostics.

smooth_response(x) = exp(0.2 * x)
kink_response(x) = abs(x)

forward_difference(f, x, h) = (f(x + h) - f(x)) / h
backward_difference(f, x, h) = (f(x) - f(x - h)) / h
central_difference(f, x, h) = (f(x + h) - f(x - h)) / (2h)

function emit(name, f, x0)
    h_values = [1.0, 0.5, 0.25, 0.125, 0.0625]
    for h in h_values
        fwd = forward_difference(f, x0, h)
        bwd = backward_difference(f, x0, h)
        cen = central_difference(f, x0, h)
        gap = abs(fwd - bwd)
        flag = gap > 0.5
        println("$name,$x0,$h,$fwd,$bwd,$cen,$gap,$flag")
    end
end

println("function_name,x0,h,forward,backward,central,one_sided_gap,kink_flag")
emit("smooth_exp_response", smooth_response, 5.0)
emit("kink_abs_response", kink_response, 0.0)
