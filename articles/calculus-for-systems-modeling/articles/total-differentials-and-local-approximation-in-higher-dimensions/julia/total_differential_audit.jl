f(x, y) = 3.0*x + 2.0*y + 0.5*x*y
fx(x, y) = 3.0 + 0.5*y
fy(x, y) = 2.0 + 0.5*x
total_differential(x, y, dx, dy) = fx(x, y)*dx + fy(x, y)*dy
feasible_displacement(x, y, dx, dy; budget=10.0) = x >= 0 && y >= 0 && x + y <= budget && x + dx >= 0 && y + dy >= 0 && x + dx + y + dy <= budget

println("x,y,dx,dy,baseline_output,actual_output,actual_change,differential_estimate,absolute_error,feasible_displacement,warning")
for case in [(4.0,3.0,0.2,-0.1),(4.0,3.0,1.0,1.0),(8.0,1.0,1.0,1.0)]
    x,y,dx,dy = case
    baseline = f(x,y)
    actual = f(x+dx,y+dy)
    actual_change = actual - baseline
    estimate = total_differential(x,y,dx,dy)
    feasible = feasible_displacement(x,y,dx,dy)
    warning = feasible ? "" : "Displacement is outside the feasible region."
    println("$x,$y,$dx,$dy,$baseline,$actual,$actual_change,$estimate,$(abs(actual_change-estimate)),$feasible,$warning")
end
