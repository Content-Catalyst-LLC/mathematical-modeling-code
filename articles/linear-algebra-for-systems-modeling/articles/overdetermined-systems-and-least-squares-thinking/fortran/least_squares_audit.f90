program least_squares_audit
  implicit none
  integer :: row_count
  integer :: column_count
  integer :: rank_value
  logical :: overdetermined
  real :: residual_norm

  row_count = 4
  column_count = 2
  rank_value = 2
  overdetermined = .true.
  residual_norm = 0.191311

  print *, "system_name row_count column_count overdetermined rank residual_norm"
  print *, "four_observation_linear_calibration", row_count, column_count, overdetermined, rank_value, residual_norm
end program least_squares_audit
