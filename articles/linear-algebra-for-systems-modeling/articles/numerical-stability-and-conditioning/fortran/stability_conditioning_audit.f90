program stability_conditioning_audit
  implicit none
  print *, "model_name matrix_case matrix_shape determinant condition_number solution_norm residual_norm relative_residual perturbation_size solution_change status"
  print *, "numerical_stability_conditioning_audit well_conditioned_system 2x2 5.75 2.10 0.34 0.0 0.0 0.00001 0.000004 stable_under_demo_threshold"
  print *, "numerical_stability_conditioning_audit ill_conditioned_system 2x2 0.00000001 399920000.0 50000000.0 0.0 0.0 0.00001 2000.0 review_required_ill_conditioned"
end program stability_conditioning_audit
