program equation_logic_resource_model
  implicit none

  integer :: period, periods, activations
  real(8) :: stock, capacity, inflow, demand, loss_rate, threshold, demand_reduction
  real(8) :: losses, raw_next, shortage, total_shortage

  stock = 40.0d0
  capacity = 60.0d0
  inflow = 3.0d0
  demand = 7.0d0
  loss_rate = 0.050d0
  threshold = 25.0d0
  demand_reduction = 1.0d0
  periods = 60
  total_shortage = 0.0d0
  activations = 0

  do period = 0, periods
    losses = loss_rate * stock
    raw_next = stock + inflow - demand - losses
    shortage = max(0.0d0, -raw_next)
    total_shortage = total_shortage + shortage

    if (stock < threshold) then
      activations = activations + 1
      demand = max(0.0d0, demand - demand_reduction)
    end if

    stock = min(capacity, max(0.0d0, raw_next))
  end do

  print '(A,F12.6,A,F12.6,A,I0)', 'fortran final_stock=', stock, ' total_shortage=', total_shortage, ' logic_activations=', activations
end program equation_logic_resource_model
