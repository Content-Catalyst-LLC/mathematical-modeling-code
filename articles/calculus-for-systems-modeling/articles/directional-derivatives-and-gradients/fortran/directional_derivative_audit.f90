program directional_derivative_audit
  implicit none
  real(8), dimension(3) :: xs, ys, vxs, vys, steps
  real(8) :: x, y, vx, vy, ux, uy, norm_value, deriv, estimated, actual, error_value
  integer :: i
  logical :: feasible

  xs = (/4.0d0, 4.0d0, 8.0d0/)
  ys = (/3.0d0, 3.0d0, 1.0d0/)
  vxs = (/1.0d0, 2.0d0, 1.0d0/)
  vys = (/1.0d0, -1.0d0, 1.0d0/)
  steps = (/0.25d0, 0.25d0, 1.0d0/)

  print '(A)', 'x y vx vy ux uy gradient_x gradient_y derivative step estimated actual error feasible'

  do i=1,3
    x = xs(i)
    y = ys(i)
    vx = vxs(i)
    vy = vys(i)
    norm_value = sqrt(vx*vx + vy*vy)
    ux = vx / norm_value
    uy = vy / norm_value
    deriv = gx(x,y)*ux + gy(x,y)*uy
    estimated = steps(i) * deriv
    actual = f(x+steps(i)*ux, y+steps(i)*uy) - f(x,y)
    error_value = abs(actual - estimated)
    feasible = x >= 0.0d0 .and. y >= 0.0d0 .and. x + y <= 10.0d0 .and. x + steps(i)*ux >= 0.0d0 .and. y + steps(i)*uy >= 0.0d0 .and. x + steps(i)*ux + y + steps(i)*uy <= 10.0d0
    if (feasible) then
      print '(14F12.6,1X,A)', x, y, vx, vy, ux, uy, gx(x,y), gy(x,y), deriv, steps(i), estimated, actual, error_value, 1.0d0, 'feasible'
    else
      print '(14F12.6,1X,A)', x, y, vx, vy, ux, uy, gx(x,y), gy(x,y), deriv, steps(i), estimated, actual, error_value, 0.0d0, 'infeasible'
    end if
  end do

contains
  function f(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = 3.0d0*x + 2.0d0*y + 0.5d0*x*y
  end function f

  function gx(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = 3.0d0 + 0.5d0*y
  end function gx

  function gy(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = 2.0d0 + 0.5d0*x
  end function gy
end program
