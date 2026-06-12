program reservoir_model
  implicit none

  integer :: period, periods
  real(8) :: storage, capacity, inflow, base_demand, demand_growth, loss_rate
  real(8) :: demand, losses, shortage, total_shortage

  storage = 80.0d0
  capacity = 100.0d0
  inflow = 8.0d0
  base_demand = 6.0d0
  demand_growth = 0.010d0
  loss_rate = 0.015d0
  periods = 60
  total_shortage = 0.0d0

  do period = 0, periods
    demand = base_demand * (1.0d0 + demand_growth) ** period
    losses = loss_rate * storage
    shortage = max(0.0d0, demand + losses - (storage + inflow))
    total_shortage = total_shortage + shortage
    storage = min(capacity, max(0.0d0, storage + inflow - demand - losses))
  end do

  print '(A,F12.6,A,F12.6)', 'fortran final_storage=', storage, ' total_shortage=', total_shortage
end program reservoir_model
