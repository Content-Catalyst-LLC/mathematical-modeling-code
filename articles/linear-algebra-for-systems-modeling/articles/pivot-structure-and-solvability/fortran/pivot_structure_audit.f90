program pivot_structure_audit
  implicit none
  integer :: equation_count
  integer :: unknown_count
  integer :: coefficient_rank
  integer :: augmented_rank
  logical :: consistent
  real :: tolerance

  equation_count = 3
  unknown_count = 3
  coefficient_rank = 3
  augmented_rank = 3
  consistent = .true.
  tolerance = 1.0e-10

  print *, "system_name equation_count unknown_count coefficient_rank augmented_rank consistent tolerance"
  print *, "three_constraint_resource_balance_system", equation_count, unknown_count, coefficient_rank, augmented_rank, consistent, tolerance
end program pivot_structure_audit
