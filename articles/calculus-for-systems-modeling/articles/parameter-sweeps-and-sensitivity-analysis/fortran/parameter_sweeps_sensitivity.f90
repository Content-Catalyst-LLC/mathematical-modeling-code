program parameter_sweeps_sensitivity
  implicit none
  integer :: i, j
  real(8), dimension(5) :: rates
  real(8), dimension(4) :: caps
  real(8) :: value

  rates = (/0.18d0, 0.25d0, 0.35d0, 0.45d0, 0.55d0/)
  caps = (/80.0d0, 100.0d0, 125.0d0, 150.0d0/)

  print '(A)', 'growth_rate carrying_capacity initial_value stop_time final_value'
  do i = 1, 5
    do j = 1, 4
      value = logistic(20.0d0, 10.0d0, rates(i), caps(j))
      print '(5F16.8)', rates(i), caps(j), 10.0d0, 20.0d0, value
    end do
  end do

contains
  real(8) function logistic(t, x0, r, k)
    real(8), intent(in) :: t, x0, r, k
    logistic = k / (1.0d0 + ((k - x0) / x0) * exp(-r * t))
  end function
end program
