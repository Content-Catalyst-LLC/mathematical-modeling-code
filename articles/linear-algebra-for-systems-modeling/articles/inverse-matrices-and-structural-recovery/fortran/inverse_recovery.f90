program inverse_recovery
  implicit none

  real :: a, b, c, d, y1, y2, det, x1, x2

  a = 3.0
  b = 1.0
  c = 2.0
  d = 4.0
  y1 = 7.0
  y2 = 8.0

  det = a * d - b * c

  if (det == 0.0) then
    print *, "Matrix is singular; recovery is not unique."
  else
    x1 = (d * y1 - b * y2) / det
    x2 = (-c * y1 + a * y2) / det
    print *, "Recovered state:"
    print *, "x1 =", x1
    print *, "x2 =", x2
  end if
end program inverse_recovery
