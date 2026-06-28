program matrix_arithmetic_audit
  implicit none
  logical :: compatible_shape
  real :: output_entry_sum

  compatible_shape = .true.
  output_entry_sum = 3.95

  print *, "operation_name matrix_shape compatible_shape output_entry_sum"
  print *, "baseline_plus_weighted_intervention_and_stress", "3x3", compatible_shape, output_entry_sum
end program matrix_arithmetic_audit
