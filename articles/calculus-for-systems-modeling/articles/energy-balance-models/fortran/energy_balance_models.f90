program energy_balance_models
  implicit none
  real(8) :: forcing, feedback, heat_capacity, equilibrium, tau
  forcing = 3.7d0
  feedback = 1.2d0
  heat_capacity = 10.0d0
  equilibrium = forcing / feedback
  tau = heat_capacity / feedback
  print '(A)', 'scenario equilibrium_temperature adjustment_time'
  print '(A,1X,F12.6,1X,F12.6)', 'baseline_one_layer', equilibrium, tau
end program
