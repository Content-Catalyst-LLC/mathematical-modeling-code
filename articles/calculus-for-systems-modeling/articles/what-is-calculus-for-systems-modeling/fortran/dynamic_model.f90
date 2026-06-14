program dynamic_model
  implicit none

  print '(A)', 'scenario final_state'
  print '(A,1X,F10.6)', 'baseline', simulate(10.0d0, 0.20d0, 100.0d0, 0.1d0, 300)
  print '(A,1X,F10.6)', 'slow_adjustment', simulate(10.0d0, 0.10d0, 100.0d0, 0.1d0, 300)
  print '(A,1X,F10.6)', 'high_capacity', simulate(10.0d0, 0.20d0, 140.0d0, 0.1d0, 300)

contains

  real(8) function simulate(initial_state, rate, capacity, dt, steps)
    real(8), intent(in) :: initial_state, rate, capacity, dt
    integer, intent(in) :: steps
    integer :: i
    real(8) :: state, derivative

    state = initial_state
    do i = 1, steps
      derivative = rate * state * (1.0d0 - state / capacity)
      state = max(0.0d0, state + derivative * dt)
    end do
    simulate = state
  end function simulate

end program dynamic_model
