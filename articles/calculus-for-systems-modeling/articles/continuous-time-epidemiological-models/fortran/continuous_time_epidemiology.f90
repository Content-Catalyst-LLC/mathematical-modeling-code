program continuous_time_epidemiology
  implicit none
  real(8) :: beta, gamma, r0, dt
  beta = 0.32d0
  gamma = 0.10d0
  r0 = beta / gamma
  dt = log(2.0d0) / (beta - gamma)
  print '(A)', 'scenario reproduction_number doubling_time'
  print '(A,1X,F12.6,1X,F12.6)', 'baseline_sir', r0, dt
end program
