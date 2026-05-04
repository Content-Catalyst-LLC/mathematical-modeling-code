program numerical_methods
  implicit none

  integer, parameter :: intervals = 500
  integer :: i
  real :: start_value, end_value, width, x0, x1, y0, y1, total

  start_value = 0.0
  end_value = 10.0
  width = (end_value - start_value) / intervals
  total = 0.0

  do i = 1, intervals
    x0 = start_value + (i - 1) * width
    x1 = start_value + i * width
    y0 = sin(x0) + 1.5
    y1 = sin(x1) + 1.5
    total = total + 0.5 * (y0 + y1) * width
  end do

  print *, "Trapezoid integral estimate:", total

end program numerical_methods
