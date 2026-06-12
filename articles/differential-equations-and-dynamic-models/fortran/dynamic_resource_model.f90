program dynamic_resource_model
  implicit none

  integer :: step, steps
  real(8) :: storage, capacity, inflow_rate, demand_rate, loss_rate, dt, horizon, time
  real(8) :: rate, raw_next, shortage, overflow, total_shortage, total_overflow

  storage = 80.0d0
  capacity = 100.0d0
  inflow_rate = 8.0d0
  demand_rate = 6.0d0
  loss_rate = 0.015d0
  dt = 0.25d0
  horizon = 60.0d0
  steps = int(horizon / dt)
  time = 0.0d0
  total_shortage = 0.0d0
  total_overflow = 0.0d0

  do step = 0, steps
    rate = inflow_rate - demand_rate - loss_rate * storage
    raw_next = storage + dt * rate
    shortage = max(0.0d0, -raw_next)
    overflow = max(0.0d0, raw_next - capacity)
    total_shortage = total_shortage + shortage
    total_overflow = total_overflow + overflow
    storage = min(capacity, max(0.0d0, raw_next))
    time = time + dt
  end do

  print '(A,F12.6,A,F12.6,A,F12.6)', 'fortran final_storage=', storage, ' total_shortage=', total_shortage, ' total_overflow=', total_overflow
end program dynamic_resource_model
