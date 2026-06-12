program model_purpose_resource_model
  implicit none

  integer :: period, periods
  real(8) :: stock, capacity, inflow, demand, control_action, effective_demand, loss_rate
  real(8) :: losses, shortage, total_shortage

  stock = 80.0d0
  capacity = 100.0d0
  inflow = 5.0d0
  demand = 6.0d0
  control_action = 1.5d0
  loss_rate = 0.015d0
  periods = 60
  total_shortage = 0.0d0

  do period = 0, periods
    effective_demand = max(0.0d0, demand - control_action)
    losses = loss_rate * stock
    shortage = max(0.0d0, effective_demand + losses - (stock + inflow))
    total_shortage = total_shortage + shortage
    stock = min(capacity, max(0.0d0, stock + inflow - effective_demand - losses))
  end do

  print '(A,F12.6,A,F12.6)', 'fortran final_stock=', stock, ' total_shortage=', total_shortage
end program model_purpose_resource_model
