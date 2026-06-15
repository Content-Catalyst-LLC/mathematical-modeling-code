program rate_diagnostics
  implicit none
  real(8), dimension(5) :: hs
  real(8) :: x,h,exact,est
  integer :: i
  hs = (/1.0d0,0.5d0,0.25d0,0.125d0,0.0625d0/)
  x = 5.0d0
  exact = exact_derivative(x)
  print '(A)', 'method x0 h estimate exact absolute_error elasticity'
  do i=1,size(hs)
    h=hs(i)
    est=average_rate(x,x+h); call emit('average_rate_right',x,h,est,exact)
    est=forward_difference(x,h); call emit('forward_difference',x,h,est,exact)
    est=backward_difference(x,h); call emit('backward_difference',x,h,est,exact)
    est=central_difference(x,h); call emit('central_difference',x,h,est,exact)
  end do
contains
  real(8) function system_response(x)
    real(8), intent(in) :: x
    system_response=exp(0.2d0*x)
  end function
  real(8) function exact_derivative(x)
    real(8), intent(in) :: x
    exact_derivative=0.2d0*exp(0.2d0*x)
  end function
  real(8) function average_rate(a,b)
    real(8), intent(in) :: a,b
    average_rate=(system_response(b)-system_response(a))/(b-a)
  end function
  real(8) function forward_difference(x,h)
    real(8), intent(in) :: x,h
    forward_difference=(system_response(x+h)-system_response(x))/h
  end function
  real(8) function backward_difference(x,h)
    real(8), intent(in) :: x,h
    backward_difference=(system_response(x)-system_response(x-h))/h
  end function
  real(8) function central_difference(x,h)
    real(8), intent(in) :: x,h
    central_difference=(system_response(x+h)-system_response(x-h))/(2.0d0*h)
  end function
  real(8) function elasticity(d,x)
    real(8), intent(in) :: d,x
    elasticity=(x/system_response(x))*d
  end function
  subroutine emit(name,x,h,est,exact)
    character(len=*), intent(in) :: name
    real(8), intent(in) :: x,h,est,exact
    print '(A,1X,F8.4,1X,F8.4,1X,F14.8,1X,F14.8,1X,F14.8,1X,F14.8)', trim(name),x,h,est,exact,abs(est-exact),elasticity(est,x)
  end subroutine
end program
