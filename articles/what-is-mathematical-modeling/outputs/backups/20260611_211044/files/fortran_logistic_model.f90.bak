program logistic_model
  implicit none
  integer :: step, steps
  real(8) :: x, r, k, dt

  x = 10.0d0
  r = 0.35d0
  k = 100.0d0
  dt = 0.1d0
  steps = 160

  do step = 0, steps
    if (mod(step, 40) == 0) then
      print '(A,I4,A,F8.3,A,F12.6)', 'step=', step, ' time=', step * dt, ' state=', x
    end if
    x = rk4_step(x, r, k, dt)
  end do

  print '(A,F12.6)', 'Fortran RK4 final_state=', x

contains

  real(8) function deriv(x, r, k)
    real(8), intent(in) :: x, r, k
    deriv = r * x * (1.0d0 - x / k)
  end function deriv

  real(8) function rk4_step(x, r, k, dt)
    real(8), intent(in) :: x, r, k, dt
    real(8) :: k1, k2, k3, k4
    k1 = deriv(x, r, k)
    k2 = deriv(x + 0.5d0 * dt * k1, r, k)
    k3 = deriv(x + 0.5d0 * dt * k2, r, k)
    k4 = deriv(x + dt * k3, r, k)
    rk4_step = max(0.0d0, x + (dt / 6.0d0) * (k1 + 2.0d0*k2 + 2.0d0*k3 + k4))
  end function rk4_step

end program logistic_model
