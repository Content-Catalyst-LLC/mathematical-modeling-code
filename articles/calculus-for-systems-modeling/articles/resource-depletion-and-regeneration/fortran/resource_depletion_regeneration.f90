program resource_depletion_regeneration
  implicit none
  integer :: i
  real(8) :: stock, harvest, dt, extraction, growth, cumulative
  stock = 600.0d0
  harvest = 35.0d0
  dt = 0.1d0
  cumulative = 0.0d0
  do i = 1, 800
    extraction = min(stock, harvest * dt)
    growth = max(0.0d0, 0.18d0 * stock * (1.0d0 - stock / 1000.0d0)) * dt
    stock = max(0.0d0, stock + growth - extraction)
    cumulative = cumulative + extraction
  end do
  print '(A)', 'scenario_name resource_type final_stock cumulative_extraction warning'
  print '(A,1X,A,1X,F12.6,1X,F12.6,1X,A)', 'renewable_precautionary_harvest','renewable_logistic',stock,cumulative,'precautionary_harvest'
end program
