program policy_option_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: projected_benefit(n), total_cost(n), feasibility(n), equity_score(n), uncertainty_width(n), public_risk(n)
  real(8) :: scores(n)
  integer :: i

  keys = (/ 'baseline                      ', 'targeted_prevention           ', 'broad_expansion               ', 'adaptive_pathway              ' /)
  projected_benefit = (/ 42.0d0, 68.0d0, 81.0d0, 73.0d0 /)
  total_cost = (/ 18.0d0, 32.0d0, 49.0d0, 38.0d0 /)
  feasibility = (/ 0.86d0, 0.74d0, 0.58d0, 0.70d0 /)
  equity_score = (/ 0.52d0, 0.78d0, 0.69d0, 0.82d0 /)
  uncertainty_width = (/ 18.0d0, 22.0d0, 28.0d0, 16.0d0 /)
  public_risk = (/ 0.42d0, 0.30d0, 0.34d0, 0.24d0 /)

  print '(A)', 'key projected_benefit total_cost equity_score public_risk public_value_score budget_violation'

  do i = 1, n
    scores(i) = public_value_score(projected_benefit(i), total_cost(i), feasibility(i), equity_score(i), uncertainty_width(i), public_risk(i))
    print '(A,1X,F8.3,1X,F8.3,1X,F6.3,1X,F6.3,1X,F10.4,1X,L1)', trim(keys(i)), projected_benefit(i), total_cost(i), equity_score(i), public_risk(i), scores(i), total_cost(i) > 40.0d0
  end do

contains

  real(8) function public_value_score(benefit, cost, feasible, equity, uncertainty, risk)
    implicit none
    real(8), intent(in) :: benefit, cost, feasible, equity, uncertainty, risk
    real(8) :: budget_penalty

    if (cost > 40.0d0) then
      budget_penalty = 14.0d0
    else
      budget_penalty = 0.0d0
    end if

    public_value_score = benefit + 18.0d0 * feasible + 24.0d0 * equity - cost - 0.22d0 * uncertainty - 30.0d0 * risk - budget_penalty
  end function public_value_score

end program policy_option_summary
