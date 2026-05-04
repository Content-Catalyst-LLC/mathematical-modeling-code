program monte_carlo_mean
  implicit none

  integer, parameter :: n = 10000
  integer :: i
  real :: exposure, vulnerability, loss, total

  call random_seed()

  total = 0.0

  do i = 1, n
    call random_number(exposure)
    call random_number(vulnerability)

    exposure = 0.2 + 0.8 * exposure
    loss = exposure * vulnerability

    total = total + loss
  end do

  print *, "Monte Carlo mean loss estimate:", total / n

end program monte_carlo_mean
