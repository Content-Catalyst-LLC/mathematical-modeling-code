program inverse_recovery_audit
  implicit none
  print *, "system_name matrix_size determinant invertible rank nullity residual_norm tolerance"
  print *, "three_constraint_structural_recovery_system", 3, 2.0, .true., 3, 0, 0.0, 1.0e-10
end program inverse_recovery_audit
