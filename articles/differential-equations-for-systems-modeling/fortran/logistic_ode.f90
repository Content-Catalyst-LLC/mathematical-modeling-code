program logistic_ode
  implicit none

  integer, parameter :: steps = 300
  integer :: i
  real :: dt, growth_rate, capacity, derivative
  real, dimension(steps) :: state

  dt = 0.1
  growth_rate = 0.20
  capacity = 100.0
  state(1) = 10.0

  do i = 2, steps
    derivative = growth_rate * state(i - 1) * (1.0 - state(i - 1) / capacity)
    state(i) = state(i - 1) + derivative * dt
  end do

  print *, "Final state:", state(steps)

end program logistic_ode
