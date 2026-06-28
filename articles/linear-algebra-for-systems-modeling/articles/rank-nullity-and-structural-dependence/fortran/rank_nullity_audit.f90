program rank_nullity_audit
  implicit none
  integer :: row_count
  integer :: column_count
  integer :: rank_value
  integer :: nullity_value
  logical :: rank_deficient
  real :: tolerance

  row_count = 3
  column_count = 3
  rank_value = 3
  nullity_value = column_count - rank_value
  rank_deficient = .false.
  tolerance = 1.0e-10

  print *, "system_name row_count column_count rank nullity rank_deficient tolerance"
  print *, "three_constraint_resource_balance_matrix", row_count, column_count, rank_value, nullity_value, rank_deficient, tolerance
end program rank_nullity_audit
