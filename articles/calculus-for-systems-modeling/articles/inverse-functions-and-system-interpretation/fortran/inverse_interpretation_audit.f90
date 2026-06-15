program inverse_interpretation_audit
  implicit none
  real(8), dimension(5) :: ys
  real(8) :: y,x,ycheck,residual,derivative,invsens
  integer :: i
  ys = (/0.0d0,0.5d0,1.0d0,1.5d0,2.0d0/)
  print '(A)', 'target_output recovered_input forward_check residual forward_derivative inverse_sensitivity'
  do i=1,size(ys)
    y=ys(i); x=inverse_model(y); ycheck=forward_model(x); residual=ycheck-y
    derivative=forward_derivative(x); invsens=1.0d0/derivative
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', y,x,ycheck,residual,derivative,invsens
  end do
contains
  real(8) function forward_model(x)
    real(8), intent(in) :: x
    forward_model=log(1.0d0+x)
  end function
  real(8) function forward_derivative(x)
    real(8), intent(in) :: x
    forward_derivative=1.0d0/(1.0d0+x)
  end function
  real(8) function inverse_model(y)
    real(8), intent(in) :: y
    inverse_model=exp(y)-1.0d0
  end function
end program
