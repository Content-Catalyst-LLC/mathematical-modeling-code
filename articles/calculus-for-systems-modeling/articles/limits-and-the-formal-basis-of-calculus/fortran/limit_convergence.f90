program limit_convergence_program
  implicit none
  real(8), dimension(6) :: h_values
  real(8) :: x, h, exact, fd, cd, cd2, rich
  integer :: i

  h_values = (/ 1.0d0, 0.5d0, 0.25d0, 0.125d0, 0.0625d0, 0.03125d0 /)
  x = 5.0d0
  exact = exact_derivative(x)

  print '(A)', 'method x h estimate exact absolute_error'

  do i = 1, size(h_values)
    h = h_values(i)
    fd = forward_difference(x, h)
    cd = central_difference(x, h)
    cd2 = central_difference(x, h / 2.0d0)
    rich = richardson(cd, cd2)
    print '(A,1X,F8.4,1X,F10.6,1X,F14.8,1X,F14.8,1X,F14.8)', 'forward_difference', x, h, fd, exact, abs(fd - exact)
    print '(A,1X,F8.4,1X,F10.6,1X,F14.8,1X,F14.8,1X,F14.8)', 'central_difference', x, h, cd, exact, abs(cd - exact)
    print '(A,1X,F8.4,1X,F10.6,1X,F14.8,1X,F14.8,1X,F14.8)', 'richardson_central', x, h, rich, exact, abs(rich - exact)
  end do

contains

  real(8) function f(x)
    real(8), intent(in) :: x
    f = exp(0.2d0 * x)
  end function f

  real(8) function exact_derivative(x)
    real(8), intent(in) :: x
    exact_derivative = 0.2d0 * exp(0.2d0 * x)
  end function exact_derivative

  real(8) function forward_difference(x, h)
    real(8), intent(in) :: x, h
    forward_difference = (f(x + h) - f(x)) / h
  end function forward_difference

  real(8) function central_difference(x, h)
    real(8), intent(in) :: x, h
    central_difference = (f(x + h) - f(x - h)) / (2.0d0 * h)
  end function central_difference

  real(8) function richardson(central_h, central_h2)
    real(8), intent(in) :: central_h, central_h2
    richardson = (4.0d0 * central_h2 - central_h) / 3.0d0
  end function richardson

end program limit_convergence_program
