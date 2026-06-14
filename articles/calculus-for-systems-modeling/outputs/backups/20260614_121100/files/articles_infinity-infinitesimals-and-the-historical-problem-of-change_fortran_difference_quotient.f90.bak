program difference_quotient_program
  implicit none
  real(8), dimension(7) :: h_values
  real(8) :: x, h, exact, estimate
  integer :: i

  h_values = (/ 1.0d0, 0.5d0, 0.1d0, 0.05d0, 0.01d0, 0.005d0, 0.001d0 /)
  x = 5.0d0
  exact = exact_derivative(x)

  print '(A)', 'function_name x h estimate exact_value absolute_error'

  do i = 1, size(h_values)
    h = h_values(i)
    estimate = difference_quotient(x, h)
    print '(A,1X,F8.4,1X,F8.4,1X,F14.8,1X,F14.8,1X,F14.8)', 'exp(0.2x)', x, h, estimate, exact, abs(estimate - exact)
  end do

contains

  real(8) function system_response(x)
    real(8), intent(in) :: x
    system_response = exp(0.2d0 * x)
  end function system_response

  real(8) function exact_derivative(x)
    real(8), intent(in) :: x
    exact_derivative = 0.2d0 * exp(0.2d0 * x)
  end function exact_derivative

  real(8) function difference_quotient(x, h)
    real(8), intent(in) :: x, h
    difference_quotient = (system_response(x + h) - system_response(x)) / h
  end function difference_quotient

end program difference_quotient_program
