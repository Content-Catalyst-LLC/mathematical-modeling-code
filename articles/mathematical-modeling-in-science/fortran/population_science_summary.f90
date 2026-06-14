program population_science_summary
  implicit none

  integer, parameter :: n = 5
  character(len=32) :: keys(n)
  real(8) :: growth_rate(n), carrying_capacity(n), initial_population(n), final_population(n)
  integer :: years(n), i

  keys = (/ 'baseline                      ', 'lower_growth                  ', 'higher_growth                 ', 'lower_capacity                ', 'higher_capacity               ' /)
  growth_rate = (/ 0.28d0, 0.18d0, 0.38d0, 0.28d0, 0.28d0 /)
  carrying_capacity = (/ 500.0d0, 500.0d0, 500.0d0, 350.0d0, 700.0d0 /)
  initial_population = (/ 40.0d0, 40.0d0, 40.0d0, 40.0d0, 40.0d0 /)
  years = (/ 20, 20, 20, 20, 20 /)

  print '(A)', 'key growth_rate carrying_capacity initial_population years final_population crosses_capacity_midpoint'

  do i = 1, n
    final_population(i) = logistic_final(initial_population(i), growth_rate(i), carrying_capacity(i), years(i))
    print '(A,1X,F6.3,1X,F8.2,1X,F8.2,1X,I3,1X,F10.4,1X,L1)', trim(keys(i)), growth_rate(i), carrying_capacity(i), initial_population(i), years(i), final_population(i), final_population(i) >= carrying_capacity(i) / 2.0d0
  end do

contains

  real(8) function logistic_final(initial, growth, capacity, n_years)
    implicit none
    real(8), intent(in) :: initial, growth, capacity
    integer, intent(in) :: n_years
    integer :: year
    real(8) :: population

    population = initial
    do year = 1, n_years
      population = population + growth * population * (1.0d0 - population / capacity)
    end do
    logistic_final = population
  end function logistic_final

end program population_science_summary
