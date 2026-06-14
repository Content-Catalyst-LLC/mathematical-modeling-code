program ai_candidate_governance_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: validation(n), calibration(n), subgroup_gap(n), drift(n), interpretability(n), privacy(n), criticality(n)
  real(8) :: score(n)
  integer :: i
  logical :: review

  keys = (/ 'baseline_logistic              ', 'tree_ensemble                  ', &
            'neural_model                   ', 'constrained_model              ' /)
  validation = (/ 0.76d0, 0.83d0, 0.86d0, 0.81d0 /)
  calibration = (/ 0.050d0, 0.070d0, 0.095d0, 0.035d0 /)
  subgroup_gap = (/ 0.080d0, 0.140d0, 0.190d0, 0.060d0 /)
  drift = (/ 0.120d0, 0.180d0, 0.240d0, 0.100d0 /)
  interpretability = (/ 0.920d0, 0.620d0, 0.380d0, 0.780d0 /)
  privacy = (/ 0.080d0, 0.130d0, 0.180d0, 0.090d0 /)
  criticality = (/ 0.620d0, 0.700d0, 0.820d0, 0.660d0 /)

  print '(A)', 'key validation_score calibration_error subgroup_error_gap drift_score privacy_risk governance_score requires_review'

  do i = 1, n
    score(i) = governance_score(validation(i), calibration(i), subgroup_gap(i), drift(i), interpretability(i), privacy(i), criticality(i))
    review = calibration(i) > 0.08d0 .or. subgroup_gap(i) > 0.12d0 .or. drift(i) > 0.20d0 .or. privacy(i) > 0.15d0 .or. interpretability(i) < 0.50d0
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F10.4,1X,L1)', &
      trim(keys(i)), validation(i), calibration(i), subgroup_gap(i), drift(i), privacy(i), score(i), review
  end do

contains

  real(8) function governance_score(validation, calibration, subgroup_gap, drift, interpretability, privacy, criticality)
    implicit none
    real(8), intent(in) :: validation, calibration, subgroup_gap, drift, interpretability, privacy, criticality
    governance_score = validation - (1.8d0 * calibration + 1.5d0 * subgroup_gap + 1.2d0 * drift + 1.4d0 * privacy + 0.7d0 * criticality - 0.5d0 * interpretability)
  end function governance_score

end program ai_candidate_governance_summary
