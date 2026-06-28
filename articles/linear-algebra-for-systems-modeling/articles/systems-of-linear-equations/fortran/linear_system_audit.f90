program linear_system_audit
  implicit none
  integer :: equation_count
  integer :: unknown_count
  integer :: coefficient_rank
  integer :: augmented_rank
  logical :: consistent

  equation_count = 3
  unknown_count = 3
  coefficient_rank = 3
  augmented_rank = 3
  consistent = .true.

  print *, "system_name equation_count unknown_count coefficient_rank augmented_rank consistent"
  print *, "three_constraint_resource_balance_system", equation_count, unknown_count, coefficient_rank, augmented_rank, consistent
end program linear_system_audit
