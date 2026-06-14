program epidemic_scenario_summary
  implicit none

  integer, parameter :: n = 4
  character(len=40) :: keys(n)
  real(8) :: population(n), initial_infectious(n), initial_recovered(n)
  real(8) :: beta(n), gamma(n), hospital_capacity(n), hospitalization_rate(n)
  real(8) :: r0(n), peak_infectious(n), peak_hospital(n), capacity_margin(n)
  integer :: days(n), i
  logical :: breach

  keys = (/ 'baseline                                ', 'moderate_intervention                   ', &
            'strong_intervention                     ', 'vaccination_plus_intervention           ' /)
  population = (/ 100000.0d0, 100000.0d0, 100000.0d0, 100000.0d0 /)
  initial_infectious = (/ 120.0d0, 120.0d0, 120.0d0, 120.0d0 /)
  initial_recovered = (/ 4000.0d0, 4000.0d0, 4000.0d0, 22000.0d0 /)
  beta = (/ 0.32d0, 0.24d0, 0.18d0, 0.20d0 /)
  gamma = (/ 0.12d0, 0.12d0, 0.12d0, 0.12d0 /)
  days = (/ 120, 120, 120, 120 /)
  hospital_capacity = (/ 850.0d0, 850.0d0, 850.0d0, 850.0d0 /)
  hospitalization_rate = (/ 0.045d0, 0.045d0, 0.045d0, 0.030d0 /)

  print '(A)', 'key r0_simple peak_infectious peak_hospital_demand capacity_margin capacity_breach'

  do i = 1, n
    call evaluate_sir(population(i), initial_infectious(i), initial_recovered(i), beta(i), gamma(i), &
      days(i), hospital_capacity(i), hospitalization_rate(i), r0(i), peak_infectious(i), peak_hospital(i), capacity_margin(i))
    breach = peak_hospital(i) > hospital_capacity(i)
    print '(A,1X,F8.4,1X,F12.3,1X,F12.3,1X,F12.3,1X,L1)', trim(keys(i)), &
      r0(i), peak_infectious(i), peak_hospital(i), capacity_margin(i), breach
  end do

contains

  subroutine evaluate_sir(population, initial_infectious, initial_recovered, beta, gamma, days, &
      hospital_capacity, hospitalization_rate, r0_simple, peak_infectious, peak_hospital_demand, capacity_margin)
    implicit none
    real(8), intent(in) :: population, initial_infectious, initial_recovered, beta, gamma
    integer, intent(in) :: days
    real(8), intent(in) :: hospital_capacity, hospitalization_rate
    real(8), intent(out) :: r0_simple, peak_infectious, peak_hospital_demand, capacity_margin
    real(8) :: susceptible, infectious, recovered, new_infections, new_recoveries, hospital_demand
    integer :: day

    susceptible = population - initial_infectious - initial_recovered
    infectious = initial_infectious
    recovered = initial_recovered
    peak_infectious = infectious
    peak_hospital_demand = infectious * hospitalization_rate

    do day = 1, days
      new_infections = beta * susceptible * infectious / population
      new_recoveries = gamma * infectious
      susceptible = max(0.0d0, susceptible - new_infections)
      infectious = max(0.0d0, infectious + new_infections - new_recoveries)
      recovered = min(population, recovered + new_recoveries)
      peak_infectious = max(peak_infectious, infectious)
      hospital_demand = infectious * hospitalization_rate
      peak_hospital_demand = max(peak_hospital_demand, hospital_demand)
    end do

    r0_simple = beta / gamma
    capacity_margin = hospital_capacity - peak_hospital_demand
  end subroutine evaluate_sir

end program epidemic_scenario_summary
