program decision_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: expected_stock(n), lower_bound(n), burden(n), consequence(n), scores(n)
  integer :: i

  keys = (/ 'no_action                      ', 'monitoring                     ', 'moderate_intervention          ', 'strong_intervention            ' /)
  expected_stock = (/ 52.0d0, 54.0d0, 60.0d0, 68.0d0 /)
  lower_bound = (/ 38.0d0, 42.0d0, 50.0d0, 58.0d0 /)
  burden = (/ 1.0d0, 3.0d0, 5.0d0, 8.0d0 /)
  consequence = (/ 9.0d0, 6.0d0, 4.0d0, 2.0d0 /)

  print '(A)', 'key decision_score threshold_margin robustness_class'

  do i = 1, n
    scores(i) = decision_score(expected_stock(i), lower_bound(i), burden(i), consequence(i))
    if (lower_bound(i) >= 45.0d0) then
      print '(A,1X,F8.3,1X,F8.3,1X,A)', trim(keys(i)), scores(i), expected_stock(i) - 45.0d0, 'robust'
    else
      print '(A,1X,F8.3,1X,F8.3,1X,A)', trim(keys(i)), scores(i), expected_stock(i) - 45.0d0, 'fragile'
    end if
  end do

contains

  real(8) function decision_score(expected, lower, implementation_burden, consequence_if_wrong)
    implicit none
    real(8), intent(in) :: expected, lower, implementation_burden, consequence_if_wrong
    real(8) :: threshold_penalty

    if (lower < 45.0d0) then
      threshold_penalty = 8.0d0
    else
      threshold_penalty = 0.0d0
    end if

    decision_score = expected - 0.8d0 * implementation_burden - 1.2d0 * consequence_if_wrong - threshold_penalty
  end function decision_score

end program decision_summary
