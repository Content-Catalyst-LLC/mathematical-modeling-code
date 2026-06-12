program model_selection_summary
  implicit none

  integer, parameter :: n = 5
  integer :: i, best_index
  character(len=32) :: model_id(n)
  real(8) :: calibration_rmse(n), validation_rmse(n), interpretability(n), robustness(n), decision_relevance(n)
  integer :: parameter_count(n)
  real(8) :: current_score, best_score, overfit_gap

  model_id = (/ 'baseline_naive                  ', 'linear_trend                    ', 'logistic_growth                 ', 'stochastic_shock                ', 'high_flex_curve                 ' /)
  calibration_rmse = (/2.90d0, 1.80d0, 1.25d0, 1.05d0, 0.45d0/)
  validation_rmse = (/3.05d0, 2.10d0, 1.42d0, 1.60d0, 2.75d0/)
  parameter_count = (/0, 2, 3, 6, 9/)
  interpretability = (/0.95d0, 0.88d0, 0.76d0, 0.58d0, 0.35d0/)
  robustness = (/0.72d0, 0.70d0, 0.82d0, 0.88d0, 0.40d0/)
  decision_relevance = (/0.55d0, 0.68d0, 0.86d0, 0.90d0, 0.52d0/)

  best_score = huge(1.0d0)
  best_index = 1

  print '(A)', 'model_id comparison_score overfit_gap'

  do i = 1, n
    current_score = validation_rmse(i) + 0.08d0 * real(parameter_count(i), 8) &
      - 0.35d0 * interpretability(i) - 0.40d0 * robustness(i) - 0.35d0 * decision_relevance(i)
    overfit_gap = validation_rmse(i) - calibration_rmse(i)
    print '(A,1X,F8.4,1X,F8.4)', trim(model_id(i)), current_score, overfit_gap
    if (current_score < best_score) then
      best_score = current_score
      best_index = i
    end if
  end do

  print '(A,1X,A)', 'selected_model', trim(model_id(best_index))

end program model_selection_summary
