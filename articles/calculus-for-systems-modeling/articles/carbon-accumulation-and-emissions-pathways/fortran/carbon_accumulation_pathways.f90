program carbon_accumulation_pathways
  implicit none
  integer :: y, years
  real(8) :: e0, cumulative, emission
  e0 = 40.0d0
  years = 30
  cumulative = 0.0d0
  do y = 0, years
    emission = max(0.0d0, e0 * (1.0d0 - dble(y) / dble(years)))
    cumulative = cumulative + emission
  end do
  print '(A)', 'scenario_name pathway_type cumulative_emissions warning'
  print '(A,1X,A,1X,F12.6,1X,A)', 'linear_decline_to_zero','linear_decline',cumulative,'linear_decline_still_accumulates_until_net_zero'
end program
