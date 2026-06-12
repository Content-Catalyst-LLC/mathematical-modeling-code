program state_representation_resource_model
  implicit none

  integer :: period, periods
  real(8) :: storage, demand, condition, capacity, inflow, loss_rate, demand_response, condition_decay
  real(8) :: effective_loss_rate, losses, raw_next, shortage, total_shortage

  storage = 45.0d0
  demand = 8.0d0
  condition = 0.85d0
  capacity = 80.0d0
  inflow = 4.0d0
  loss_rate = 0.020d0
  demand_response = 0.20d0
  condition_decay = 0.002d0
  periods = 60
  total_shortage = 0.0d0

  do period = 0, periods
    effective_loss_rate = loss_rate * (1.0d0 + (1.0d0 - condition))
    losses = effective_loss_rate * storage
    raw_next = storage + inflow - demand - losses
    shortage = max(0.0d0, -raw_next)
    total_shortage = total_shortage + shortage

    demand = max(0.0d0, demand - demand_response * shortage)
    condition = max(0.0d0, condition - condition_decay * shortage)
    storage = min(capacity, max(0.0d0, raw_next))
  end do

  print '(A,F12.6,A,F12.6,A,F12.6,A,F12.6)', 'fortran final_storage=', storage, ' final_demand=', demand, ' final_condition=', condition, ' total_shortage=', total_shortage
end program state_representation_resource_model
