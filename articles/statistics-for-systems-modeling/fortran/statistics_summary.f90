program statistics_summary
  implicit none

  integer, parameter :: n = 10
  real, dimension(n) :: values
  real :: mean_value, variance_value, sd_value
  integer :: i

  values = (/18.4, 36.7, 62.1, 28.9, 64.8, 13.7, 43.5, 29.8, 79.4, 30.2/)

  mean_value = sum(values) / n
  variance_value = 0.0

  do i = 1, n
    variance_value = variance_value + (values(i) - mean_value)**2
  end do

  variance_value = variance_value / (n - 1)
  sd_value = sqrt(variance_value)

  print *, "Mean:", mean_value
  print *, "Sample variance:", variance_value
  print *, "Sample standard deviation:", sd_value

end program statistics_summary
