program delay_memory_audit
  implicit none
  integer, parameter :: steps = 300
  integer :: step, delay_steps, delayed_index
  real(8) :: initial_state, target, adjustment_rate, delay, dt, time, current, delayed, derivative
  real(8), dimension(0:steps+1) :: states

  initial_state = 80.0d0
  target = 100.0d0
  adjustment_rate = 0.2d0
  delay = 5.0d0
  dt = 0.1d0
  delay_steps = nint(delay / dt)
  states(0) = initial_state

  print '(A)', 'step time current_state delayed_state derivative_value target absolute_gap'
  do step = 0, steps
    time = dble(step) * dt
    current = states(step)
    delayed_index = step - delay_steps
    if (delayed_index < 0) then
      delayed = initial_state
    else
      delayed = states(delayed_index)
    end if
    derivative = adjustment_rate * (target - delayed)
    print '(I6,6F14.6)', step, time, current, delayed, derivative, target, abs(current - target)
    states(step + 1) = current + dt * derivative
  end do
end program
