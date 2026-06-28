program state_vector_audit
  implicit none
  real :: a, b, c, d, tr, det, disc, root, lambda1, lambda2, dominant
  a = 0.80
  b = 0.15
  c = 0.20
  d = 0.90
  tr = a + d
  det = a * d - b * c
  disc = tr * tr - 4.0 * det
  root = sqrt(disc)
  lambda1 = (tr + root) / 2.0
  lambda2 = (tr - root) / 2.0
  dominant = max(abs(lambda1), abs(lambda2))
  print *, 'model_name rank determinant dominant_eigenvalue warning'
  print *, 'two_component_transition_model', 2, det, dominant, 'Matrix interpretation depends on entry meaning and scale.'
end program state_vector_audit
