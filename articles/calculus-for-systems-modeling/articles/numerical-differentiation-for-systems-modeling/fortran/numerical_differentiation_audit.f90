program numerical_differentiation_audit
  implicit none
  integer, parameter :: n = 100
  integer :: i
  real(8) :: start, h, x, value, true_d, forward, backward, central, err
  real(8), dimension(0:n) :: xs, values

  start = 0.0d0
  h = 0.1d0

  do i = 0, n
    xs(i) = start + dble(i) * h
    values(i) = sin(xs(i)) + 0.1d0 * xs(i) * xs(i)
  end do

  print '(A)', 'index x value true_derivative forward_difference backward_difference central_difference central_absolute_error step_size'
  do i = 0, n
    x = xs(i)
    value = values(i)
    true_d = cos(x) + 0.2d0 * x
    forward = 0.0d0
    backward = 0.0d0
    central = 0.0d0
    err = 0.0d0

    if (i < n) forward = (values(i+1) - values(i)) / h
    if (i > 0) backward = (values(i) - values(i-1)) / h
    if (i > 0 .and. i < n) then
      central = (values(i+1) - values(i-1)) / (2.0d0*h)
      err = abs(central - true_d)
    end if

    print '(I6,8F16.8)', i, x, value, true_d, forward, backward, central, err, h
  end do
end program
