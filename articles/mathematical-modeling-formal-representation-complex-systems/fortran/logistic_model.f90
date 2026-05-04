program logistic_model
  implicit none

  integer, parameter :: time_steps = 80
  integer :: t
  real :: growth_rate, carrying_capacity
  real, dimension(time_steps) :: state

  growth_rate = 0.18
  carrying_capacity = 100.0
  state(1) = 10.0

  do t = 2, time_steps
    state(t) = state(t - 1) + growth_rate * state(t - 1) * (1.0 - state(t - 1) / carrying_capacity)
  end do

  print *, "Final state:", state(time_steps)

end program logistic_model
