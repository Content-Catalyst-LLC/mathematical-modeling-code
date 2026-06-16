program financial_dynamics_compounding
  implicit none
  real(8) :: fv, pv
  fv = 1000.0d0 * exp(0.05d0 * 30.0d0)
  pv = 5000.0d0 * exp(-0.05d0 * 30.0d0)
  print '(A)', 'scenario final_value present_value'
  print '(A,1X,F12.6,1X,F12.6)', 'continuous_compounding_case', fv, 1000.0d0
  print '(A,1X,F12.6,1X,F12.6)', 'discounted_future_value', 5000.0d0, pv
end program
