program static_allocation_model
  implicit none

  real(8) :: budget, cost_a, cost_b, benefit_a, benefit_b
  real(8) :: allocation_a, allocation_b, capacity_a, capacity_b
  real(8) :: total_cost, total_benefit, benefit_per_cost, budget_slack
  logical :: feasible

  budget = 100.0d0
  cost_a = 4.0d0
  cost_b = 5.0d0
  benefit_a = 8.0d0
  benefit_b = 11.0d0
  allocation_a = 10.0d0
  allocation_b = 8.0d0
  capacity_a = 20.0d0
  capacity_b = 15.0d0

  total_cost = cost_a * allocation_a + cost_b * allocation_b
  total_benefit = benefit_a * allocation_a + benefit_b * allocation_b
  benefit_per_cost = total_benefit / total_cost
  budget_slack = budget - total_cost
  feasible = budget_slack >= 0.0d0 .and. capacity_a - allocation_a >= 0.0d0 .and. capacity_b - allocation_b >= 0.0d0

  print '(A,F12.6,A,F12.6,A,F12.6,A,F12.6,A,L1)', 'fortran total_cost=', total_cost, ' total_benefit=', total_benefit, ' benefit_per_cost=', benefit_per_cost, ' budget_slack=', budget_slack, ' feasible=', feasible
end program static_allocation_model
