program elasticity_sensitivity_audit
  implicit none
  real(8), dimension(6) :: xs
  real(8) :: x
  integer :: i
  xs = (/0.0d0,0.5d0,1.0d0,4.0d0,9.0d0,24.0d0/)
  print '(A)', 'x value derivative elasticity'
  do i=1,size(xs)
    x=xs(i)
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6)', x, response_function(x), analytic_derivative(x), elasticity_value(x)
  end do
contains
  real(8) function response_function(x)
    real(8), intent(in) :: x
    response_function=10.0d0*sqrt(x+1.0d0)
  end function
  real(8) function analytic_derivative(x)
    real(8), intent(in) :: x
    analytic_derivative=5.0d0/sqrt(x+1.0d0)
  end function
  real(8) function elasticity_value(x)
    real(8), intent(in) :: x
    real(8) :: y
    y=response_function(x)
    if (x == 0.0d0 .or. y == 0.0d0) then
      elasticity_value=0.0d0
    else
      elasticity_value=(x/y)*analytic_derivative(x)
    end if
  end function
end program
