program inverse_recovery_diagnostics
  implicit none

  real :: a, b, c, d, y1, y2, det, x1, x2
  real :: r1, r2, residual_norm

  a = 3.0
  b = 1.0
  c = 2.0
  d = 4.0
  y1 = 7.0
  y2 = 8.0

  det = a * d - b * c
  print *, "det(A) =", det

  if (abs(det) < 1.0e-12) then
    print *, "Matrix is singular or numerically near-singular."
    stop 1
  end if

  x1 = (d * y1 - b * y2) / det
  x2 = (-c * y1 + a * y2) / det

  r1 = a * x1 + b * x2 - y1
  r2 = c * x1 + d * x2 - y2
  residual_norm = sqrt(r1 * r1 + r2 * r2)

  print *, "Recovered state:"
  print *, "x1 =", x1
  print *, "x2 =", x2
  print *, "Residual norm =", residual_norm
end program inverse_recovery_diagnostics
