f_model(x, y) = x^2 + x*y + 3*y^2 + 0.2*x^2*y
gradient(x, y) = (2*x + y + 0.4*x*y, x + 6*y + 0.2*x^2)
hessian(x, y) = [2 + 0.4*y 1 + 0.4*x; 1 + 0.4*x 6.0]
det2(H) = H[1,1]*H[2,2] - H[1,2]*H[2,1]
function classify_hessian(H)
    d = det2(H)
    if d > 0 && H[1,1] > 0
        return "positive definite"
    elseif d > 0 && H[1,1] < 0
        return "negative definite"
    elseif d < 0
        return "indefinite"
    else
        return "semidefinite or inconclusive"
    end
end

println("x,y,dx,dy,gradient_x,gradient_y,h11,h12,h21,h22,determinant,trace,classification,first_order_change,second_order_change,actual_change,first_order_error,second_order_error,warning")
for case in [(2.0,1.0,0.1,-0.05),(2.0,1.0,0.5,0.5),(-5.0,0.0,0.2,0.1)]
    x,y,dx,dy = case
    gx,gy = gradient(x,y)
    H = hessian(x,y)
    detv = det2(H)
    classv = classify_hessian(H)
    first = gx*dx + gy*dy
    quad = 0.5 * (H[1,1]*dx*dx + 2*H[1,2]*dx*dy + H[2,2]*dy*dy)
    second = first + quad
    actual = f_model(x+dx,y+dy) - f_model(x,y)
    warning = classv == "indefinite" ? "Hessian is indefinite; local structure is saddle-like." : (abs(detv) < 1e-8 ? "Hessian is singular or nearly singular." : "")
    println("$x,$y,$dx,$dy,$gx,$gy,$(H[1,1]),$(H[1,2]),$(H[2,1]),$(H[2,2]),$detv,$(H[1,1]+H[2,2]),$classv,$first,$second,$actual,$(abs(actual-first)),$(abs(actual-second)),$warning")
end
