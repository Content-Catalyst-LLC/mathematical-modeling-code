program governance_risk_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: error_risk(n), uncertainty(n), consequence(n), misuse(n), gap(n)
  real(8) :: score(n)
  integer :: i

  ! Assign character values individually to avoid mixed-length array constructor errors.
  keys(1) = 'infrastructure_risk'
  keys(2) = 'public_health_demand'
  keys(3) = 'supply_chain_resilience'
  keys(4) = 'ai_triage_support'

  error_risk = (/ 0.38d0, 0.50d0, 0.36d0, 0.62d0 /)
  uncertainty = (/ 0.56d0, 0.68d0, 0.52d0, 0.72d0 /)
  consequence = (/ 0.82d0, 0.86d0, 0.65d0, 0.95d0 /)
  misuse = (/ 0.42d0, 0.48d0, 0.40d0, 0.70d0 /)
  gap = (/ 0.24d0, 0.32d0, 0.22d0, 0.55d0 /)

  print '(A)', 'key error_risk uncertainty consequence scope_misuse accountability_gap governance_risk_score'

  do i = 1, n
    score(i) = governance_score(error_risk(i), uncertainty(i), consequence(i), misuse(i), gap(i))
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F10.4)', &
      trim(keys(i)), error_risk(i), uncertainty(i), consequence(i), misuse(i), gap(i), score(i)
  end do

contains

  real(8) function governance_score(error_risk, uncertainty, consequence, misuse, gap)
    implicit none
    real(8), intent(in) :: error_risk, uncertainty, consequence, misuse, gap
    governance_score = 0.20d0 * error_risk + 0.20d0 * uncertainty + 0.25d0 * consequence + 0.20d0 * misuse + 0.15d0 * gap
  end function governance_score

end program governance_risk_summary
