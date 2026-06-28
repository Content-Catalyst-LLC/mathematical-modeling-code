program linear_transformation_behavior_audit
  implicit none
  integer :: row_count
  integer :: column_count
  integer :: rank_value
  integer :: nullity_value
  real :: input_norm
  real :: output_norm
  real :: amplification_ratio

  row_count = 3
  column_count = 3
  rank_value = 3
  nullity_value = 0
  input_norm = 120.415946
  output_norm = 152.750205
  amplification_ratio = output_norm / input_norm

  print *, "system_name row_count column_count rank nullity input_norm output_norm amplification_ratio"
  print *, "three_component_system_response", row_count, column_count, rank_value, nullity_value, input_norm, output_norm, amplification_ratio
end program linear_transformation_behavior_audit
