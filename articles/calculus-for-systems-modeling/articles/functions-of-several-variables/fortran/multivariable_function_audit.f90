program multivariable_function_audit
  implicit none
  real(8), dimension(3) :: xs, ys
  real(8) :: x, y, output
  integer :: i
  logical :: feasible
  xs = (/2.0d0, 8.0d0, 6.0d0/)
  ys = (/4.0d0, 4.0d0, 3.0d0/)
  print '(A)', 'x y output feasible'
  do i=1,3
    x = xs(i); y = ys(i)
    output = 3.0d0*x + 2.0d0*y + 0.5d0*x*y
    feasible = x >= 0.0d0 .and. y >= 0.0d0 .and. x + y <= 10.0d0
    if (feasible) then
      print '(F8.3,1X,F8.3,1X,F12.6,1X,A)', x, y, output, 'feasible'
    else
      print '(F8.3,1X,F8.3,1X,F12.6,1X,A)', x, y, output, 'infeasible'
    end if
  end do
end program
