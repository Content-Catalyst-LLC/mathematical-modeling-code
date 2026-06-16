program euler_method_audit
  implicit none
  integer :: step, steps
  real(8) :: y0, k, h, stop_time, y, t, exact, multiplier

  y0 = 100.0d0
  k = 0.35d0
  h = 0.1d0
  stop_time = 20.0d0
  steps = nint(stop_time / h)
  y = y0
  multiplier = 1.0d0 - h * k

  print '(A)', 'step time euler_value exact_value absolute_error step_size stability_multiplier'
  do step = 0, steps
    t = dble(step) * h
    exact = y0 * exp(-k * t)
    print '(I6,6F16.8)', step, t, y, exact, abs(y - exact), h, multiplier
    y = y + h * (-k * y)
  end do
end program
