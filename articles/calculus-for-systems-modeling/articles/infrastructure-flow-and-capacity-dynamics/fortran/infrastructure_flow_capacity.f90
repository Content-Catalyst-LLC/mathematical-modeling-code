program infrastructure_flow_capacity
  implicit none
  real(8), dimension(3) :: arrivals
  real(8) :: u, delay
  integer :: i
  arrivals = (/75.0d0, 95.0d0, 115.0d0/)
  print '(A)', 'scenario utilization delay_warning'
  do i = 1, 3
    u = arrivals(i) / 100.0d0
    if (u >= 1.0d0) then
      delay = 999.0d0
    else
      delay = 1.0d0 + 0.8d0 * (u / (1.0d0 - u))
    end if
    print '(I0,1X,F12.6,1X,F12.6)', i, u, delay
  end do
end program
