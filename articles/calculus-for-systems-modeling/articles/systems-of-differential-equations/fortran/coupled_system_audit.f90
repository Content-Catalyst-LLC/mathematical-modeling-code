program coupled_system_audit
  implicit none
  real(8) :: prey, predator, alpha, beta, delta, gamma, dt, t, prey_rate, predator_rate
  integer :: n, steps
  prey = 40.0d0; predator = 9.0d0; alpha = 0.7d0; beta = 0.05d0; delta = 0.02d0; gamma = 0.5d0; dt = 0.01d0; steps = 2000
  print '(A)', 'scenario time prey predator prey_rate predator_rate alpha beta delta gamma method'
  do n = 0, steps
    t = n*dt
    prey_rate = alpha*prey - beta*prey*predator
    predator_rate = delta*prey*predator - gamma*predator
    print '(A,9F12.6,1X,A)', 'predator_prey_coupled_system', t, prey, predator, prey_rate, predator_rate, alpha, beta, delta, gamma, 'explicit_euler'
    prey = max(0.0d0, prey + dt*prey_rate)
    predator = max(0.0d0, predator + dt*predator_rate)
  end do
end program
