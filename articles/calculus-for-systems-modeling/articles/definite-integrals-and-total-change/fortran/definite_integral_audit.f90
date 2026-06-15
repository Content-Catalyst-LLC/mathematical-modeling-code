program definite_integral_audit
  implicit none
  real(8), dimension(9) :: times
  real(8) :: signed_accumulation, absolute_accumulation, dt, r0, r1
  integer :: i
  times = (/0.0d0,0.5d0,1.0d0,1.5d0,2.0d0,2.5d0,3.0d0,3.5d0,4.0d0/)
  signed_accumulation = 0.0d0
  absolute_accumulation = 0.0d0

  do i=1,8
    dt = times(i+1) - times(i)
    r0 = net_rate(times(i))
    r1 = net_rate(times(i+1))
    signed_accumulation = signed_accumulation + 0.5d0 * (r0 + r1) * dt
    absolute_accumulation = absolute_accumulation + 0.5d0 * (abs(r0) + abs(r1)) * dt
  end do

  print '(A)', 'interval_start interval_end signed_accumulation absolute_accumulation'
  print '(F8.3,1X,F8.3,1X,F14.6,1X,F14.6)', times(1), times(9), signed_accumulation, absolute_accumulation

contains
  real(8) function net_rate(t)
    real(8), intent(in) :: t
    net_rate = 4.0d0 * sin(t / 2.0d0) + 1.0d0
  end function
end program
