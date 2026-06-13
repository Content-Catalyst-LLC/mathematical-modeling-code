program generalization_summary
  implicit none

  integer, parameter :: n = 5
  integer :: i, best_index
  character(len=32) :: model_id(n)
  character(len=32) :: class_label
  real(8) :: training_rmse(n), validation_rmse(n), complexity(n), interpretability(n)
  integer :: parameter_count(n)
  real(8) :: current_score, best_score, gap

  model_id = (/ 'constant_baseline               ', 'linear_trend                    ', 'logistic_growth                 ', 'regularized_curve               ', 'high_flex_curve                 ' /)
  training_rmse = (/3.40d0, 1.95d0, 1.20d0, 0.95d0, 0.28d0/)
  validation_rmse = (/3.55d0, 2.10d0, 1.38d0, 1.44d0, 2.85d0/)
  parameter_count = (/0, 2, 3, 5, 10/)
  complexity = (/0.05d0, 0.25d0, 0.45d0, 0.62d0, 0.95d0/)
  interpretability = (/0.95d0, 0.88d0, 0.78d0, 0.66d0, 0.30d0/)

  best_score = huge(1.0d0)
  best_index = 1

  print '(A)', 'model_id generalization_score overfit_gap classification'

  do i = 1, n
    current_score = validation_rmse(i) + 0.20d0 * complexity(i) &
      + 0.08d0 * real(parameter_count(i), 8) - 0.20d0 * interpretability(i)
    gap = validation_rmse(i) - training_rmse(i)

    if (training_rmse(i) >= 3.0d0 .and. validation_rmse(i) >= 3.0d0) then
      class_label = 'likely_underfit'
    else if (gap >= 1.0d0 .and. training_rmse(i) <= 1.0d0) then
      class_label = 'likely_overfit'
    else if (validation_rmse(i) <= 1.5d0 .and. gap <= 0.6d0) then
      class_label = 'generalizes_reasonably'
    else
      class_label = 'requires_review'
    end if

    print '(A,1X,F8.4,1X,F8.4,1X,A)', trim(model_id(i)), current_score, gap, trim(class_label)
    if (current_score < best_score) then
      best_score = current_score
      best_index = i
    end if
  end do

  print '(A,1X,A)', 'selected_for_review', trim(model_id(best_index))

end program generalization_summary
