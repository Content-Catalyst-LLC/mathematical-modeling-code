program matrix_vector_multiply
  implicit none

  real, dimension(3,3) :: A
  real, dimension(3) :: x, y
  integer :: i, j

  A = reshape((/ &
    0.82, 0.12, 0.06, &
    0.10, 0.76, 0.18, &
    0.08, 0.12, 0.76 /), shape(A))

  x = (/0.70, 0.20, 0.10/)
  y = 0.0

  do i = 1, 3
    do j = 1, 3
      y(i) = y(i) + A(i,j) * x(j)
    end do
  end do

  print *, "Transformed state:", y

end program matrix_vector_multiply
