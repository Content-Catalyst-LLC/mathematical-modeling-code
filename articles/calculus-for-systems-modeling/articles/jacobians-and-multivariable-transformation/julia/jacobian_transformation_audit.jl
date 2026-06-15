F_model(x, y) = (x^2 + y, x*y + 3*y)
jacobian(x, y) = [2*x 1; y x+3]
determinant_2x2(J) = J[1,1]*J[2,2] - J[1,2]*J[2,1]

println("x,y,dx,dy,j11,j12,j21,j22,determinant,approximate_change_1,approximate_change_2,actual_change_1,actual_change_2,error_norm,warning")
for case in [(2.0,1.0,0.1,-0.05),(2.0,1.0,0.5,0.5),(0.0,0.0,0.1,0.1)]
    x,y,dx,dy = case
    J = jacobian(x,y)
    baseline = F_model(x,y)
    actual = F_model(x+dx,y+dy)
    approx1 = J[1,1]*dx + J[1,2]*dy
    approx2 = J[2,1]*dx + J[2,2]*dy
    actual1 = actual[1] - baseline[1]
    actual2 = actual[2] - baseline[2]
    detv = determinant_2x2(J)
    err = sqrt((actual1-approx1)^2 + (actual2-approx2)^2)
    warning = abs(detv) > 1e-8 ? "" : "Jacobian is singular or near singular."
    println("$x,$y,$dx,$dy,$(J[1,1]),$(J[1,2]),$(J[2,1]),$(J[2,2]),$detv,$approx1,$approx2,$actual1,$actual2,$err,$warning")
end
