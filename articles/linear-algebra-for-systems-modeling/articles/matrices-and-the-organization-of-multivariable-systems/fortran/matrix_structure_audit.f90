program matrix_structure_audit
  implicit none
  integer :: row_count
  integer :: column_count
  integer :: nonzero_entries
  integer :: rank_value
  real :: sparsity_ratio
  logical :: symmetric

  row_count = 4
  column_count = 4
  nonzero_entries = 8
  sparsity_ratio = 0.5
  symmetric = .true.
  rank_value = 4

  print *, "matrix_name row_count column_count nonzero_entries sparsity_ratio symmetric rank"
  print *, "infrastructure_interdependency_matrix", row_count, column_count, nonzero_entries, sparsity_ratio, symmetric, rank_value
end program matrix_structure_audit
