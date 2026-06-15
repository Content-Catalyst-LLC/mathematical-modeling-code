program forced_system_shock_audit
  implicit none
  integer :: step
  real(8) :: baseline, forced, equilibrium, recovery_rate, shock_time, shock_magnitude, dt, time, shock
  baseline = 100.0d0
  forced = 100.0d0
  equilibrium = 100.0d0
  recovery_rate = 0.15d0
  shock_time = 10.0d0
  shock_magnitude = -30.0d0
  dt = 0.1d0
  print '(A)', 'step time baseline_state forced_state shock_value absolute_deviation'
  do step = 0, 300
    time = dble(step) * dt
    shock = impulse_shock(time, shock_time, shock_magnitude)
    print '(I6,5F14.6)', step, time, baseline, forced, shock, abs(forced - baseline)
    baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate)
    if (shock /= 0.0d0) forced = forced + shock
    forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate)
  end do
contains
  real(8) function restoring_rate(x, equilibrium, recovery_rate)
    real(8), intent(in) :: x, equilibrium, recovery_rate
    restoring_rate = -recovery_rate * (x - equilibrium)
  end function
  real(8) function impulse_shock(time, shock_time, shock_magnitude)
    real(8), intent(in) :: time, shock_time, shock_magnitude
    if (abs(time - shock_time) < 1.0d-12) then
      impulse_shock = shock_magnitude
    else
      impulse_shock = 0.0d0
    end if
  end function
end program
