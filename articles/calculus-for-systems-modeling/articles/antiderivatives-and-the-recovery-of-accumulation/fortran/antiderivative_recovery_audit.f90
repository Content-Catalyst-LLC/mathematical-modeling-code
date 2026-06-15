program antiderivative_recovery_audit
  implicit none
  real(8), dimension(7) :: times
  real(8) :: stock, previous, current, dt, area
  integer :: i
  times = (/0.0d0,1.0d0,2.0d0,3.0d0,4.0d0,5.0d0,6.0d0/)
  stock = 100.0d0
  print '(A)', 'time net_flow recovered_stock method_code'
  print '(F8.3,1X,F14.6,1X,F14.6,1X,I2)', times(1), net_flow(times(1)), stock, 0
  do i=2,size(times)
    previous = times(i-1)
    current = times(i)
    dt = current - previous
    area = 0.5d0 * (net_flow(previous) + net_flow(current)) * dt
    stock = stock + area
    print '(F8.3,1X,F14.6,1X,F14.6,1X,I2)', current, net_flow(current), stock, 1
  end do
contains
  real(8) function net_flow(t)
    real(8), intent(in) :: t
    net_flow = (12.0d0 + 0.5d0*t) - (7.0d0 + 0.2d0*t)
  end function
end program
