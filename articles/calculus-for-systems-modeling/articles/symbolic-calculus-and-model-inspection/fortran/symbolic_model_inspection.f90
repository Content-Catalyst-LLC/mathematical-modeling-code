program symbolic_model_inspection
  implicit none
  print '(A)', 'item expression interpretation warning'
  print '(A)', 'rate_expression r*x*(1 - x/K) Logistic_growth_rate_expression K_must_be_nonzero'
  print '(A)', 'first_derivative r - 2*r*x/K Marginal_growth_declines_with_x Domain_assumptions_required'
  print '(A)', 'second_derivative -2*r/K Curvature_record Empirical_validity_not_implied'
  print '(A)', 'equilibria x=0_or_x=K Candidate_steady_states Stability_review_required'
  print '(A)', 'limit_at_capacity 0 Growth_approaches_zero Boundary_review_required'
end program
