program modeling_population_dynamics
  implicit none
  integer :: t
  real(8) :: n0,r,k,expn,logn
  n0=100.0d0; r=0.08d0; k=1000.0d0
  print '(A)', 'time exponential logistic'
  do t=0,40,5
    expn=n0*exp(r*dble(t))
    logn=k/(1.0d0+((k-n0)/n0)*exp(-r*dble(t)))
    print '(I0,1X,F12.6,1X,F12.6)', t, expn, logn
  end do
end program
