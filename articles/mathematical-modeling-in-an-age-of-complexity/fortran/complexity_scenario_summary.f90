program complexity_scenario_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: stress(n), interdependence(n), uncertainty(n), resilience(n), equity(n), adaptability(n)
  real(8) :: fragility(n), robust(n)
  integer :: i

  keys = (/ 'baseline                      ', 'compound_shock                ', &
            'cascading_failure             ', 'adaptive_pathway              ' /)

  stress = (/ 0.35d0, 0.78d0, 0.88d0, 0.65d0 /)
  interdependence = (/ 0.45d0, 0.70d0, 0.86d0, 0.68d0 /)
  uncertainty = (/ 0.40d0, 0.72d0, 0.75d0, 0.70d0 /)
  resilience = (/ 0.72d0, 0.48d0, 0.32d0, 0.66d0 /)
  equity = (/ 0.68d0, 0.52d0, 0.40d0, 0.70d0 /)
  adaptability = (/ 0.65d0, 0.55d0, 0.42d0, 0.82d0 /)

  print '(A)', 'key stress interdependence uncertainty resilience equity adaptability fragility robust_value'

  do i = 1, n
    fragility(i) = fragility_score(stress(i), interdependence(i), uncertainty(i), adaptability(i))
    robust(i) = robust_value(resilience(i), equity(i), adaptability(i), fragility(i))
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F10.4,1X,F10.4)', &
      trim(keys(i)), stress(i), interdependence(i), uncertainty(i), resilience(i), equity(i), adaptability(i), fragility(i), robust(i)
  end do

contains

  real(8) function fragility_score(stress, interdependence, uncertainty, adaptability)
    implicit none
    real(8), intent(in) :: stress, interdependence, uncertainty, adaptability
    fragility_score = 0.35d0 * stress + 0.30d0 * interdependence + 0.25d0 * uncertainty + 0.10d0 * (1.0d0 - adaptability)
  end function fragility_score

  real(8) function robust_value(resilience, equity, adaptability, fragility)
    implicit none
    real(8), intent(in) :: resilience, equity, adaptability, fragility
    robust_value = 0.40d0 * resilience + 0.30d0 * equity + 0.30d0 * adaptability - 0.20d0 * fragility
  end function robust_value

end program complexity_scenario_summary
