program flow_to_stock_audit
  implicit none
  real(8), dimension(5) :: duration, inflow, outflow, exposure, population
  real(8) :: initial_stock, cumulative_in, cumulative_out, net, ending_stock
  real(8) :: cumulative_exposure, pop_exposure, gross
  integer :: i

  duration = (/1.0d0,1.0d0,1.0d0,1.0d0,1.0d0/)
  inflow = (/12.0d0,10.0d0,9.0d0,8.0d0,7.0d0/)
  outflow = (/6.0d0,7.0d0,8.0d0,9.0d0,9.0d0/)
  exposure = (/20.0d0,18.0d0,15.0d0,13.0d0,11.0d0/)
  population = (/1000.0d0,1100.0d0,1050.0d0,980.0d0,960.0d0/)
  initial_stock = 50.0d0

  cumulative_in = 0.0d0
  cumulative_out = 0.0d0
  cumulative_exposure = 0.0d0
  pop_exposure = 0.0d0

  do i=1,5
    cumulative_in = cumulative_in + inflow(i)*duration(i)
    cumulative_out = cumulative_out + outflow(i)*duration(i)
    cumulative_exposure = cumulative_exposure + exposure(i)*duration(i)
    pop_exposure = pop_exposure + exposure(i)*population(i)*duration(i)
  end do

  net = cumulative_in - cumulative_out
  ending_stock = initial_stock + net
  gross = cumulative_in + cumulative_out

  print '(A)', 'initial_stock cumulative_inflow cumulative_outflow net_accumulation ending_stock cumulative_exposure population_weighted_exposure gross_activity'
  print '(F10.3,1X,F10.3,1X,F10.3,1X,F10.3,1X,F10.3,1X,F10.3,1X,F14.3,1X,F10.3)', initial_stock,cumulative_in,cumulative_out,net,ending_stock,cumulative_exposure,pop_exposure,gross
end program
