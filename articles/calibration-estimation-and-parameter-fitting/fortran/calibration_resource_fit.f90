program calibration_resource_fit
  implicit none

  integer, parameter :: n = 10
  real(8) :: stock(n), extraction(n)
  real(8) :: g, k, sse, best_sse, best_g, best_k

  stock = (/70.0d0,72.8d0,74.1d0,75.0d0,75.5d0,75.2d0,74.7d0,73.8d0,72.6d0,71.2d0/)
  extraction = (/5.5d0,5.8d0,6.2d0,6.4d0,6.8d0,7.0d0,7.1d0,7.4d0,7.6d0,7.8d0/)

  best_sse = huge(1.0d0)
  best_g = 0.0d0
  best_k = 0.0d0

  do g = 0.08d0, 0.26d0, 0.01d0
    do k = 85.0d0, 125.0d0, 5.0d0
      sse = score(g, k, stock, extraction, n)
      if (sse < best_sse) then
        best_sse = sse
        best_g = g
        best_k = k
      end if
    end do
  end do

  print '(A)', 'best_growth_rate best_carrying_capacity sse'
  print '(F8.4,1X,F10.4,1X,F10.4)', best_g, best_k, best_sse

contains

  real(8) function score(growth_rate, carrying_capacity, observed_stock, extraction_data, count)
    real(8), intent(in) :: growth_rate, carrying_capacity
    real(8), intent(in) :: observed_stock(count), extraction_data(count)
    integer, intent(in) :: count
    integer :: i
    real(8) :: current_stock, predicted, growth, residual

    current_stock = observed_stock(1)
    score = 0.0d0

    do i = 1, count
      predicted = current_stock
      if (i > 1) then
        growth = growth_rate * current_stock * (1.0d0 - current_stock / carrying_capacity)
        predicted = max(0.0d0, current_stock + growth - extraction_data(i - 1))
        current_stock = predicted
      end if
      residual = observed_stock(i) - predicted
      score = score + residual * residual
    end do
  end function score

end program calibration_resource_fit
