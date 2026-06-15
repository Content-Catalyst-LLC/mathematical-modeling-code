program product_rule_demo
  implicit none
  real :: a, b, da, db, ca, cb
  a = 120.0
  b = 1.5
  da = 4.0
  db = 0.03
  ca = da * b
  cb = a * db
  print *, "contribution_from_a=", ca
  print *, "contribution_from_b=", cb
  print *, "total_derivative=", ca + cb
end program product_rule_demo
