program chain_rule_pathway_audit
  implicit none
  real(8), dimension(5) :: ts
  real(8) :: t,e,c,f,temp,s1,s2,s3,s4,total
  integer :: i
  ts = (/0.0d0,5.0d0,10.0d0,20.0d0,40.0d0/)
  print '(A)', 't emissions concentration forcing temperature emissions_rate d_concentration_d_emissions d_forcing_d_concentration d_temperature_d_forcing total_derivative'
  do i=1,size(ts)
    t=ts(i); e=emissions(t); c=concentration(e); f=forcing(c); temp=temperature_response(f)
    s1=emissions_rate(t); s2=d_concentration_d_emissions(e); s3=d_forcing_d_concentration(c); s4=d_temperature_d_forcing(f)
    total=s4*s3*s2*s1
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', t,e,c,f,temp,s1,s2,s3,s4,total
  end do
contains
  real(8) function emissions(t)
    real(8), intent(in) :: t
    emissions=50.0d0*exp(0.015d0*t)
  end function
  real(8) function emissions_rate(t)
    real(8), intent(in) :: t
    emissions_rate=0.015d0*emissions(t)
  end function
  real(8) function concentration(e)
    real(8), intent(in) :: e
    concentration=0.5d0*e
  end function
  real(8) function d_concentration_d_emissions(e)
    real(8), intent(in) :: e
    d_concentration_d_emissions=0.5d0
  end function
  real(8) function forcing(c)
    real(8), intent(in) :: c
    forcing=log(1.0d0+c)
  end function
  real(8) function d_forcing_d_concentration(c)
    real(8), intent(in) :: c
    d_forcing_d_concentration=1.0d0/(1.0d0+c)
  end function
  real(8) function temperature_response(f)
    real(8), intent(in) :: f
    temperature_response=1.2d0*f
  end function
  real(8) function d_temperature_d_forcing(f)
    real(8), intent(in) :: f
    d_temperature_d_forcing=1.2d0
  end function
end program
