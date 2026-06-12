program unit_scale_resource_model
  implicit none

  integer :: period, periods
  real(8) :: storage, capacity, inflow_per_day, demand_per_day, loss_rate_per_day, delta_t_days
  real(8) :: inflow_volume, demand_volume, loss_volume, raw_next, shortage, total_shortage
  real(8) :: fraction, min_fraction, max_fraction

  storage = 80.0d0
  capacity = 100.0d0
  inflow_per_day = 8.0d0
  demand_per_day = 6.0d0
  loss_rate_per_day = 0.015d0
  delta_t_days = 1.0d0
  periods = 60
  total_shortage = 0.0d0
  min_fraction = 1.0d0
  max_fraction = 0.0d0

  do period = 0, periods
    inflow_volume = delta_t_days * inflow_per_day
    demand_volume = delta_t_days * demand_per_day
    loss_volume = delta_t_days * loss_rate_per_day * storage
    raw_next = storage + inflow_volume - demand_volume - loss_volume
    shortage = max(0.0d0, -raw_next)
    total_shortage = total_shortage + shortage
    storage = min(capacity, max(0.0d0, raw_next))
    fraction = storage / capacity
    min_fraction = min(min_fraction, fraction)
    max_fraction = max(max_fraction, fraction)
  end do

  print '(A,F12.6,A,F12.6,A,F12.6,A,F12.6)', 'fortran final_storage=', storage, ' min_fraction=', min_fraction, ' max_fraction=', max_fraction, ' total_shortage=', total_shortage
end program unit_scale_resource_model
