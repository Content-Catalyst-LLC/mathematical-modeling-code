program diagnostic_summary
  implicit none

  integer, parameter :: n = 10
  integer :: i, disagreements
  real(8) :: observed(n), predicted(n), threshold(n)
  real(8) :: residual, sum_abs, sum_sq, bias, max_abs, rmse, mae

  observed = (/82.0d0,79.5d0,77.0d0,74.3d0,71.5d0,69.2d0,67.8d0,65.5d0,63.0d0,61.1d0/)
  predicted = (/81.5d0,80.2d0,78.4d0,75.6d0,72.8d0,71.0d0,69.8d0,68.0d0,66.4d0,65.2d0/)
  threshold = (/70.0d0,70.0d0,70.0d0,70.0d0,70.0d0,70.0d0,70.0d0,70.0d0,70.0d0,70.0d0/)

  sum_abs = 0.0d0
  sum_sq = 0.0d0
  bias = 0.0d0
  max_abs = 0.0d0
  disagreements = 0

  do i = 1, n
    residual = observed(i) - predicted(i)
    sum_abs = sum_abs + abs(residual)
    sum_sq = sum_sq + residual * residual
    bias = bias + residual
    max_abs = max(max_abs, abs(residual))
    if ((observed(i) < threshold(i) .and. predicted(i) >= threshold(i)) .or. &
        (observed(i) >= threshold(i) .and. predicted(i) < threshold(i))) then
      disagreements = disagreements + 1
    end if
  end do

  rmse = sqrt(sum_sq / real(n, 8))
  mae = sum_abs / real(n, 8)
  bias = bias / real(n, 8)

  print '(A)', 'mean_error mae rmse max_abs_error decision_disagreements'
  print '(F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,I4)', bias, mae, rmse, max_abs, disagreements

end program diagnostic_summary
