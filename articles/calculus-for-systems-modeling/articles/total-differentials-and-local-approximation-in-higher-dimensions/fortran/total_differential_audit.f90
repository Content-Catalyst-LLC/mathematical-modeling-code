program total_differential_audit
  implicit none
  real(8), dimension(3) :: xs, ys, dxs, dys
  real(8) :: x, y, dx, dy, baseline, actual, change, estimate, error_value
  integer :: i
  logical :: feasible

  xs = (/4.0d0, 4.0d0, 8.0d0/)
  ys = (/3.0d0, 3.0d0, 1.0d0/)
  dxs = (/0.2d0, 1.0d0, 1.0d0/)
  dys = (/-0.1d0, 1.0d0, 1.0d0/)

  print '(A)', 'x y dx dy baseline actual change estimate error feasible'

  do i=1,3
    x = xs(i)
    y = ys(i)
    dx = dxs(i)
    dy = dys(i)
    baseline = f(x,y)
    actual = f(x+dx,y+dy)
    change = actual - baseline
    estimate = total_differential(x,y,dx,dy)
    error_value = abs(change - estimate)
    feasible = x >= 0.0d0 .and. y >= 0.0d0 .and. x + y <= 10.0d0 .and. x + dx >= 0.0d0 .and. y + dy >= 0.0d0 .and. x + dx + y + dy <= 10.0d0
    if (feasible) then
      print '(10F12.6,1X,A)', x, y, dx, dy, baseline, actual, change, estimate, error_value, 1.0d0, 'feasible'
    else
      print '(10F12.6,1X,A)', x, y, dx, dy, baseline, actual, change, estimate, error_value, 0.0d0, 'infeasible'
    end if
  end do

contains
  function f(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = 3.0d0*x + 2.0d0*y + 0.5d0*x*y
  end function f

  function fx(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = 3.0d0 + 0.5d0*y
  end function fx

  function fy(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = 2.0d0 + 0.5d0*x
  end function fy

  function total_differential(x,y,dx,dy) result(value)
    real(8), intent(in) :: x, y, dx, dy
    real(8) :: value
    value = fx(x,y)*dx + fy(x,y)*dy
  end function total_differential
end program
