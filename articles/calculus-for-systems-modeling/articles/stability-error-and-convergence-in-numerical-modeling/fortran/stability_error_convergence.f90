program stability_error_convergence
  implicit none
  integer :: i
  real(8), dimension(4) :: hs
  real(8) :: y0, k, stop_time, exact_final, numeric

  y0 = 100.0d0
  k = 0.35d0
  stop_time = 20.0d0
  hs = (/1.0d0, 0.5d0, 0.25d0, 0.125d0/)
  exact_final = y0 * exp(-k * stop_time)

  print '(A)', 'step_size steps final_numeric_value final_exact_value final_absolute_error'
  do i = 1, 4
    numeric = simulate(y0, k, hs(i), stop_time)
    print '(F10.4,I8,3F18.10)', hs(i), nint(stop_time / hs(i)), numeric, exact_final, abs(numeric - exact_final)
  end do

contains
  real(8) function rate_function(t, y, k)
    real(8), intent(in) :: t, y, k
    rate_function = -k * y
  end function

  real(8) function rk4_step(t, y, h, k)
    real(8), intent(in) :: t, y, h, k
    real(8) :: k1, k2, k3, k4
    k1 = rate_function(t, y, k)
    k2 = rate_function(t + h/2.0d0, y + h*k1/2.0d0, k)
    k3 = rate_function(t + h/2.0d0, y + h*k2/2.0d0, k)
    k4 = rate_function(t + h, y + h*k3, k)
    rk4_step = y + (h/6.0d0) * (k1 + 2.0d0*k2 + 2.0d0*k3 + k4)
  end function

  real(8) function simulate(y0, k, h, stop_time)
    real(8), intent(in) :: y0, k, h, stop_time
    integer :: step, steps
    real(8) :: y, t
    steps = nint(stop_time / h)
    y = y0
    do step = 0, steps - 1
      t = dble(step) * h
      y = rk4_step(t, y, h, k)
    end do
    simulate = y
  end function
end program
