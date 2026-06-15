program constrained_optimization_audit
  implicit none
  real(8), dimension(3) :: targets
  real(8) :: target, x, y, lambda, gfx, gfy, ggx, ggy, sx, sy, norm, cval, cres, obj
  integer :: i
  targets = (/12.0d0, 18.0d0, 24.0d0/)
  print '(A)', 'x y objective constraint_value target residual lambda grad_fx grad_fy grad_gx grad_gy stationarity_norm feasible warning'
  do i=1,3
    target = targets(i)
    y = target / 3.0d0
    x = 2.0d0 * target / 3.0d0
    lambda = 2.0d0 * x
    gfx = 2.0d0 * x
    gfy = 4.0d0 * y
    ggx = 1.0d0
    ggy = 1.0d0
    sx = gfx - lambda * ggx
    sy = gfy - lambda * ggy
    norm = sqrt(sx*sx + sy*sy)
    cval = x + y
    cres = cval - target
    obj = x*x + 2.0d0*y*y
    print '(13F12.6,1X,A)', x,y,obj,cval,target,cres,lambda,gfx,gfy,ggx,ggy,norm,1.0d0,'local_unit_dependent'
  end do
end program
