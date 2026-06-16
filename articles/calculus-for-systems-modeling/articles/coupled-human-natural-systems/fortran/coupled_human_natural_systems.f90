program coupled_human_natural_systems
  implicit none
  real(8) :: stock, growth_rate, carrying_capacity, effort, efficiency, harvest, regen
  stock = 80.0d0
  growth_rate = 0.08d0
  carrying_capacity = 100.0d0
  effort = 12.0d0
  efficiency = 0.003d0
  regen = growth_rate * stock * (1.0d0 - stock / carrying_capacity)
  harvest = efficiency * effort * stock
  print '(A)', 'scenario regeneration extraction'
  print '(A,1X,F12.6,1X,F12.6)', 'baseline_coupled_resource', regen, harvest
end program
