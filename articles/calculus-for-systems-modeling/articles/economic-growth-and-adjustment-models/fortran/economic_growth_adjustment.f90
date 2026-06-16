program economic_growth_adjustment
  implicit none
  real(8), dimension(3) :: rates
  real(8) :: g
  integer :: i
  rates = (/0.01d0, 0.025d0, 0.04d0/)
  print '(A)', 'scenario growth_rate final_output doubling_time'
  do i = 1, 3
    g = rates(i)
    print '(I0,1X,F12.6,1X,F12.6,1X,F12.6)', i, g, 100.0d0 * exp(g * 40.0d0), log(2.0d0)/g
  end do
end program
