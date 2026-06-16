program predator_prey_systems
  implicit none
  integer :: i, steps
  real(8) :: alpha, beta, gamma, delta, x, y, dt, dx, dy
  alpha = 0.6d0
  beta = 0.02d0
  gamma = 0.5d0
  delta = 0.01d0
  x = 40.0d0
  y = 9.0d0
  dt = 0.02d0
  steps = 4000
  do i = 1, steps
    dx = alpha*x - beta*x*y
    dy = delta*x*y - gamma*y
    x = max(0.0d0, x + dt*dx)
    y = max(0.0d0, y + dt*dy)
  end do
  print '(A)', 'scenario_name model_type final_prey final_predator warning'
  print '(A,1X,A,1X,F12.6,1X,F12.6,1X,A)', 'classic_lotka_volterra','lotka_volterra',x,y,'mass_action_baseline'
end program
