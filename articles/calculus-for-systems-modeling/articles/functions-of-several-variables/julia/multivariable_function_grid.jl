system_response(x, y) = 3.0*x + 2.0*y + 0.5*x*y
is_feasible(x, y; budget=10.0) = x >= 0 && y >= 0 && x + y <= budget
println("x,y,output,feasible,warning")
for x in 0:2:10, y in 0:2:10
    feasible = is_feasible(x, y)
    warning = feasible ? "" : "Input combination is outside the feasible region."
    println("$x,$y,$(system_response(x,y)),$feasible,$warning")
end
