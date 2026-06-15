f(x, y) = 3.0*x + 2.0*y + 0.5*x*y
gradient(x, y) = (3.0 + 0.5*y, 2.0 + 0.5*x)
function normalize(vx, vy)
    norm_value = sqrt(vx*vx + vy*vy)
    if norm_value == 0
        error("Direction vector must be nonzero.")
    end
    return (vx / norm_value, vy / norm_value)
end
directional_derivative(x, y, ux, uy) = gradient(x, y)[1]*ux + gradient(x, y)[2]*uy
feasible_direction(x, y, ux, uy, step; budget=10.0) = x >= 0 && y >= 0 && x + y <= budget && x + step*ux >= 0 && y + step*uy >= 0 && x + step*ux + y + step*uy <= budget

println("x,y,direction_x,direction_y,unit_x,unit_y,gradient_x,gradient_y,directional_derivative,step_size,estimated_change,actual_change,absolute_error,feasible_direction,warning")
for case in [(4.0,3.0,1.0,1.0,0.25),(4.0,3.0,2.0,-1.0,0.25),(8.0,1.0,1.0,1.0,1.0)]
    x,y,vx,vy,step = case
    ux,uy = normalize(vx,vy)
    gx,gy = gradient(x,y)
    deriv = directional_derivative(x,y,ux,uy)
    actual_change = f(x+step*ux, y+step*uy) - f(x,y)
    estimated_change = step * deriv
    feasible = feasible_direction(x,y,ux,uy,step)
    warning = feasible ? "" : "Direction and step move outside the feasible region."
    println("$x,$y,$vx,$vy,$ux,$uy,$gx,$gy,$deriv,$step,$estimated_change,$actual_change,$(abs(actual_change-estimated_change)),$feasible,$warning")
end
