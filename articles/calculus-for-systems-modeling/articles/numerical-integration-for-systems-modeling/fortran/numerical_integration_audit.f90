program numerical_integration_audit
implicit none
integer :: i
real(8) :: h,t,r,left,trap,truth
h=0.1d0; left=0.0d0; trap=0.0d0
print '(A)', 'index time rate left_cumulative trapezoid_cumulative true_cumulative'
do i=0,100
  t=dble(i)*h
  r=2.0d0+sin(t)+0.1d0*t
  if (i>0) then
    left=left+(2.0d0+sin(dble(i-1)*h)+0.1d0*dble(i-1)*h)*h
    trap=trap+0.5d0*((2.0d0+sin(dble(i-1)*h)+0.1d0*dble(i-1)*h)+r)*h
  endif
  truth=(2.0d0*t-cos(t)+1.0d0+0.05d0*t*t)
  print '(I6,5F14.6)', i,t,r,left,trap,truth
enddo
end program
