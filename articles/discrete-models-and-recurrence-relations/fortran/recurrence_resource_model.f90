program recurrence_resource_model
  implicit none

  integer :: period, periods
  real(8) :: storage, demand, capacity, inflow, loss_rate, demand_response
  real(8) :: raw_next, shortage, overflow, total_shortage, total_overflow

  storage = 45.0d0
  demand = 10.0d0
  capacity = 80.0d0
  inflow = 4.0d0
  loss_rate = 0.020d0
  demand_response = 0.20d0
  periods = 60
  total_shortage = 0.0d0
  total_overflow = 0.0d0

  do period = 0, periods
    raw_next = storage + inflow - demand - loss_rate * storage
    shortage = max(0.0d0, -raw_next)
    overflow = max(0.0d0, raw_next - capacity)
    total_shortage = total_shortage + shortage
    total_overflow = total_overflow + overflow
    demand = max(0.0d0, demand - demand_response * shortage)
    storage = min(capacity, max(0.0d0, raw_next))
  end do

  print '(A,F12.6,A,F12.6,A,F12.6,A,F12.6)', 'fortran final_storage=', storage, ' final_demand=', demand, ' total_shortage=', total_shortage, ' total_overflow=', total_overflow
end program recurrence_resource_model
