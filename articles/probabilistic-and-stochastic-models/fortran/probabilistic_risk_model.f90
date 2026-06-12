program probabilistic_risk_model
  implicit none

  integer, parameter :: simulations = 5000
  integer :: i, shortage_events
  real(8) :: demand_mu, demand_sigma, supply_mean, supply_sd, reserve
  real(8) :: demand, supply, shortage, expected_shortage, shortage_probability
  real(8) :: u1, u2, z1, z2, pi_value, max_shortage

  pi_value = 4.0d0 * atan(1.0d0)
  demand_mu = 4.50d0
  demand_sigma = 0.25d0
  supply_mean = 95.0d0
  supply_sd = 8.0d0
  reserve = 5.0d0
  expected_shortage = 0.0d0
  max_shortage = 0.0d0
  shortage_events = 0

  call random_seed()

  do i = 1, simulations
    call random_number(u1)
    call random_number(u2)
    if (u1 <= 0.0d0) u1 = 1.0d-12
    z1 = sqrt(-2.0d0 * log(u1)) * cos(2.0d0 * pi_value * u2)
    z2 = sqrt(-2.0d0 * log(u1)) * sin(2.0d0 * pi_value * u2)

    demand = exp(demand_mu + demand_sigma * z1)
    supply = max(0.0d0, supply_mean + supply_sd * z2)
    shortage = max(0.0d0, demand - (supply + reserve))

    expected_shortage = expected_shortage + shortage
    max_shortage = max(max_shortage, shortage)
    if (shortage > 0.0d0) shortage_events = shortage_events + 1
  end do

  expected_shortage = expected_shortage / simulations
  shortage_probability = dble(shortage_events) / dble(simulations)

  print '(A,F10.6,A,F12.6,A,F12.6)', 'fortran shortage_probability=', shortage_probability, ' expected_shortage=', expected_shortage, ' max_shortage=', max_shortage
end program probabilistic_risk_model
