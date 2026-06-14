program future_modeling_priority_summary
  implicit none
  integer, parameter :: n = 5
  character(len=32) :: keys(n)
  real(8) :: complexity(n), maturity(n), governance(n), uncertainty(n), judgment(n), score(n)
  integer :: i

  keys = (/ 'hybrid_models                 ', 'ai_assistance                 ', 'digital_twins                 ', 'uncertainty_workflows         ', 'participatory_modeling        ' /)
  complexity = (/ 0.88d0, 0.82d0, 0.86d0, 0.90d0, 0.78d0 /)
  maturity = (/ 0.70d0, 0.78d0, 0.75d0, 0.72d0, 0.62d0 /)
  governance = (/ 0.74d0, 0.90d0, 0.88d0, 0.82d0, 0.86d0 /)
  uncertainty = (/ 0.72d0, 0.76d0, 0.70d0, 0.92d0, 0.68d0 /)
  judgment = (/ 0.80d0, 0.92d0, 0.84d0, 0.86d0, 0.94d0 /)

  print '(A)', 'key complexity maturity governance uncertainty human_judgment future_priority_score'
  do i = 1, n
    score(i) = 0.25d0*complexity(i) + 0.20d0*maturity(i) + 0.20d0*governance(i) + 0.20d0*uncertainty(i) + 0.15d0*judgment(i)
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F10.4)', trim(keys(i)), complexity(i), maturity(i), governance(i), uncertainty(i), judgment(i), score(i)
  end do
end program future_modeling_priority_summary
