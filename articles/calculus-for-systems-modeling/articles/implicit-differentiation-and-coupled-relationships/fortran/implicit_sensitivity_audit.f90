program implicit_sensitivity_audit
  implicit none
  real(8), dimension(5) :: ps
  real(8) :: p,x,gx,gp,sens
  integer :: i
  ps = (/-3.0d0,-1.0d0,0.0d0,1.0d0,3.0d0/)
  print '(A)', 'parameter equilibrium_state constraint_value partial_state partial_parameter implicit_sensitivity'
  do i=1,size(ps)
    p=ps(i); x=equilibrium_state(p); gx=partial_state(x,p); gp=partial_parameter(x,p); sens=-gp/gx
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', p,x,constraint(x,p),gx,gp,sens
  end do
contains
  real(8) function equilibrium_state(p)
    real(8), intent(in) :: p
    equilibrium_state=(-p + sqrt(p*p + 40.0d0)) / 2.0d0
  end function
  real(8) function constraint(x,p)
    real(8), intent(in) :: x,p
    constraint=x*x + p*x - 10.0d0
  end function
  real(8) function partial_state(x,p)
    real(8), intent(in) :: x,p
    partial_state=2.0d0*x + p
  end function
  real(8) function partial_parameter(x,p)
    real(8), intent(in) :: x,p
    partial_parameter=x
  end function
end program
