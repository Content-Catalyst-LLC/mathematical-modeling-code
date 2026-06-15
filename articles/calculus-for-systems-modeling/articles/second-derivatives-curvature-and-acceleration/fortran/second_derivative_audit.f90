program second_derivative_audit
  implicit none
  real(8), dimension(7) :: xs
  real(8) :: x
  integer :: i
  xs = (/-4.0d0,-2.0d0,-1.0d0,0.0d0,1.0d0,2.0d0,4.0d0/)
  print '(A)', 'x value first_derivative second_derivative curvature'
  do i=1,size(xs)
    x=xs(i)
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', x, logistic(x), first_derivative(x), second_derivative(x), curvature_value(x)
  end do
contains
  real(8) function logistic(x)
    real(8), intent(in) :: x
    logistic=1.0d0/(1.0d0+exp(-x))
  end function
  real(8) function first_derivative(x)
    real(8), intent(in) :: x
    real(8) :: y
    y=logistic(x)
    first_derivative=y*(1.0d0-y)
  end function
  real(8) function second_derivative(x)
    real(8), intent(in) :: x
    real(8) :: y
    y=logistic(x)
    second_derivative=y*(1.0d0-y)*(1.0d0-2.0d0*y)
  end function
  real(8) function curvature_value(x)
    real(8), intent(in) :: x
    real(8) :: fp, fpp
    fp=first_derivative(x)
    fpp=second_derivative(x)
    curvature_value=abs(fpp)/((1.0d0+fp*fp)**1.5d0)
  end function
end program
