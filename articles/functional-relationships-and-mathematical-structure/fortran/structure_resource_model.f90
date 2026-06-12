program structure_resource_model
  implicit none

  integer :: period, periods
  real(8) :: stock, capacity, inflow, demand, feedback_strength, loss_rate
  real(8) :: losses, raw_next, shortage, overflow, total_shortage, total_overflow

  stock = 40.0d0
  capacity = 60.0d0
  inflow = 3.0d0
  demand = 7.0d0
  feedback_strength = 0.20d0
  loss_rate = 0.050d0
  periods = 60
  total_shortage = 0.0d0
  total_overflow = 0.0d0

  do period = 0, periods
    losses = loss_rate * stock
    raw_next = stock + inflow - demand - losses
    shortage = max(0.0d0, -raw_next)
    overflow = max(0.0d0, raw_next - capacity)
    total_shortage = total_shortage + shortage
    total_overflow = total_overflow + overflow
    stock = min(capacity, max(0.0d0, raw_next))
    demand = max(0.0d0, demand - feedback_strength * shortage)
  end do

  print '(A,F12.6,A,F12.6,A,F12.6)', 'fortran final_stock=', stock, ' total_shortage=', total_shortage, ' total_overflow=', total_overflow
end program structure_resource_model
