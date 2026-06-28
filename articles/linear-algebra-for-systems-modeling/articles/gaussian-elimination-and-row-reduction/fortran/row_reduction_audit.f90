program row_reduction_audit
  implicit none
  print *, "system_name equation_count unknown_count coefficient_rank augmented_rank consistent tolerance"
  print *, "three_constraint_resource_balance_system", 3, 3, 3, 3, .true., 1.0e-10
end program row_reduction_audit
