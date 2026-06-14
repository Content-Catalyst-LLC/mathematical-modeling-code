program model_ethics_risk_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: severity(n), likelihood(n), detectability_gap(n), uncertainty_level(n), equity_concern(n), accountability_gap(n)
  real(8) :: score(n)
  integer :: i

  keys = (/ 'exploratory_model              ', 'allocation_model               ', &
            'public_dashboard               ', 'automated_score                ' /)

  severity = (/ 0.35d0, 0.85d0, 0.70d0, 0.90d0 /)
  likelihood = (/ 0.35d0, 0.55d0, 0.50d0, 0.60d0 /)
  detectability_gap = (/ 0.25d0, 0.55d0, 0.45d0, 0.70d0 /)
  uncertainty_level = (/ 0.60d0, 0.65d0, 0.80d0, 0.60d0 /)
  equity_concern = (/ 0.30d0, 0.75d0, 0.55d0, 0.80d0 /)
  accountability_gap = (/ 0.25d0, 0.70d0, 0.60d0, 0.85d0 /)

  print '(A)', 'key severity likelihood detectability_gap uncertainty_level equity_concern accountability_gap ethical_risk_score'

  do i = 1, n
    score(i) = ethical_risk_score(severity(i), likelihood(i), detectability_gap(i), uncertainty_level(i), equity_concern(i), accountability_gap(i))
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F10.4)', &
      trim(keys(i)), severity(i), likelihood(i), detectability_gap(i), uncertainty_level(i), equity_concern(i), accountability_gap(i), score(i)
  end do

contains

  real(8) function ethical_risk_score(severity, likelihood, detectability_gap, uncertainty_level, equity_concern, accountability_gap)
    implicit none
    real(8), intent(in) :: severity, likelihood, detectability_gap, uncertainty_level, equity_concern, accountability_gap
    ethical_risk_score = 1.8d0 * severity + 1.3d0 * likelihood + 1.2d0 * detectability_gap + 1.1d0 * uncertainty_level + 1.5d0 * equity_concern + 1.6d0 * accountability_gap
  end function ethical_risk_score

end program model_ethics_risk_summary
