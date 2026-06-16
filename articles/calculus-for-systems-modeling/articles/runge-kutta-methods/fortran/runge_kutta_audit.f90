program runge_kutta_audit
  implicit none
  integer :: step, steps
  real(8) :: y0, k, h, stop_time, t, exact, euler_y, rk_y

  y0 = 100.0d0
  k = 0.35d0
  h = 0.5d0
  stop_time = 20.0d0
  steps = nint(stop_time / h)
  euler_y = y0
  rk_y = y0

  print '(A)', 'step time euler_value rk4_value exact_value euler_absolute_error rk4_absolute_error'
  do step = 0, steps
    t = dble(step) * h
    exact = y0 * exp(-k * t)
    print '(I6,6F16.8)', step, t, euler_y, rk_y, exact, abs(euler_y - exact), abs(rk_y - exact)
    euler_y = euler_y + h * (-k * euler_y)
    rk_y = rk4_next(t, rk_y, h, k)
  end do

contains
  real(8) function rate_function(t, y, k)
    real(8), intent(in) :: t, y, k
    rate_function = -k * y
  end function

  real(8) function rk4_next(t, y, h, k)
    real(8), intent(in) :: t, y, h, k
    real(8) :: k1, k2, k3, k4
    k1 = rate_function(t, y, k)
    k2 = rate_function(t + h/2.0d0, y + h*k1/2.0d0, k)
    k3 = rate_function(t + h/2.0d0, y + h*k2/2.0d0, k)
    k4 = rate_function(t + h, y + h*k3, k)
    rk4_next = y + (h/6.0d0) * (k1 + 2.0d0*k2 + 2.0d0*k3 + k4)
  end function
end program
