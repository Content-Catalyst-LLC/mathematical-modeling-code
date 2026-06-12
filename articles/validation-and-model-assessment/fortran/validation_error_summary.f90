program validation_error_summary
  implicit none

  integer, parameter :: n = 8
  integer :: i
  real(8) :: observed(n), predicted(n)
  real(8) :: residual, sum_abs, sum_sq, bias, max_abs, rmse, mae
  character(len=40) :: fitness

  observed = (/70.1d0,68.9d0,67.4d0,65.8d0,64.2d0,62.1d0,60.4d0,58.8d0/)
  predicted = (/70.8d0,69.7d0,68.3d0,66.9d0,65.1d0,63.8d0,61.3d0,59.9d0/)

  sum_abs = 0.0d0
  sum_sq = 0.0d0
  bias = 0.0d0
  max_abs = 0.0d0

  do i = 1, n
    residual = observed(i) - predicted(i)
    sum_abs = sum_abs + abs(residual)
    sum_sq = sum_sq + residual * residual
    bias = bias + residual
    max_abs = max(max_abs, abs(residual))
  end do

  rmse = sqrt(sum_sq / real(n, 8))
  mae = sum_abs / real(n, 8)
  bias = bias / real(n, 8)

  if (rmse <= 1.25d0 .and. max_abs <= 2.0d0) then
    fitness = 'adequate_for_scenario_screening'
  else if (rmse <= 2.5d0) then
    fitness = 'limited_use_requires_review'
  else
    fitness = 'not_adequate_without_revision'
  end if

  print '(A)', 'rmse mae bias max_abs_error fitness'
  print '(F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,A)', rmse, mae, bias, max_abs, trim(fitness)

end program validation_error_summary
