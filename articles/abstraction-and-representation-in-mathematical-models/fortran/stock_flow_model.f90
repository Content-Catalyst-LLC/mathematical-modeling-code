program stock_flow_model
  implicit none

  integer :: period, periods
  real(8) :: stock, capacity, inflow, demand, loss_rate
  real(8) :: losses, shortage, total_shortage

  stock = 80.0d0
  capacity = 100.0d0
  inflow = 8.0d0
  demand = 6.0d0
  loss_rate = 0.015d0
  periods = 60
  total_shortage = 0.0d0

  do period = 0, periods
    losses = loss_rate * stock
    shortage = max(0.0d0, demand + losses - (stock + inflow))
    total_shortage = total_shortage + shortage
    stock = min(capacity, max(0.0d0, stock + inflow - demand - losses))
  end do

  print '(A,F12.6,A,F12.6)', 'fortran final_stock=', stock, ' total_shortage=', total_shortage
end program stock_flow_model
