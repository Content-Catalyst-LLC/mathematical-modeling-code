program model_calibration_calculus
  implicit none
  integer :: i, j, n
  real(8), dimension(7) :: times, observed
  real(8), dimension(6) :: rates
  real(8), dimension(5) :: caps
  real(8) :: loss, abs_sum, max_abs, pred, res, ar

  times = (/0.0d0,2.0d0,4.0d0,6.0d0,8.0d0,10.0d0,12.0d0/)
  observed = (/10.0d0,17.5d0,29.2d0,44.1d0,60.5d0,74.0d0,83.2d0/)
  rates = (/0.22d0,0.26d0,0.30d0,0.34d0,0.38d0,0.42d0/)
  caps = (/85.0d0,95.0d0,105.0d0,115.0d0,125.0d0/)

  print '(A)', 'growth_rate carrying_capacity loss mean_absolute_residual max_absolute_residual'
  do i = 1, 6
    do j = 1, 5
      loss = 0.0d0
      abs_sum = 0.0d0
      max_abs = 0.0d0
      do n = 1, 7
        pred = logistic(times(n), 10.0d0, rates(i), caps(j))
        res = observed(n) - pred
        ar = abs(res)
        loss = loss + res * res
        abs_sum = abs_sum + ar
        if (ar > max_abs) max_abs = ar
      end do
      print '(5F18.8)', rates(i), caps(j), loss, abs_sum / 7.0d0, max_abs
    end do
  end do

contains
  real(8) function logistic(t, x0, r, k)
    real(8), intent(in) :: t, x0, r, k
    logistic = k / (1.0d0 + ((k - x0) / x0) * exp(-r * t))
  end function
end program
