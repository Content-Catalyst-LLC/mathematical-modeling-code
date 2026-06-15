program quotient_rule_audit
  implicit none
  real(8), dimension(5) :: ts
  real(8) :: t,f,g,fp,gp,ratio,ne,de,qd
  integer :: i
  ts = (/0.0d0,5.0d0,10.0d0,20.0d0,40.0d0/)
  print '(A)', 't numerator denominator ratio numerator_rate denominator_rate numerator_effect denominator_effect quotient_derivative ratio_relative_rate'
  do i=1,size(ts)
    t=ts(i); f=resource(t); g=population(t); fp=resource_rate(t); gp=population_rate(t)
    ratio=f/g; ne=fp/g; de=-(f*gp)/(g*g); qd=ne+de
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', t,f,g,ratio,fp,gp,ne,de,qd,qd/ratio
  end do
contains
  real(8) function resource(t)
    real(8), intent(in) :: t
    resource=1000.0d0*exp(-0.01d0*t)
  end function
  real(8) function resource_rate(t)
    real(8), intent(in) :: t
    resource_rate=-0.01d0*resource(t)
  end function
  real(8) function population(t)
    real(8), intent(in) :: t
    population=100.0d0*exp(0.02d0*t)
  end function
  real(8) function population_rate(t)
    real(8), intent(in) :: t
    population_rate=0.02d0*population(t)
  end function
end program
