program sustainability_scenario_summary
  implicit none

  integer, parameter :: n = 5
  character(len=32) :: keys(n)
  real(8) :: initial_stock(n), growth_rate(n), capacity(n), extraction(n)
  real(8) :: climate_stress(n), minimum_stock(n)
  real(8) :: final_stock(n), min_stock(n), min_margin(n)
  integer :: years(n), i
  logical :: breach

  keys = (/ 'baseline                      ', 'high_extraction               ', &
            'climate_stress                ', 'restoration_pathway           ', &
            'adaptive_management           ' /)
  initial_stock = (/ 420.0d0, 420.0d0, 420.0d0, 420.0d0, 420.0d0 /)
  growth_rate = (/ 0.24d0, 0.24d0, 0.24d0, 0.28d0, 0.25d0 /)
  capacity = (/ 800.0d0, 800.0d0, 800.0d0, 860.0d0, 820.0d0 /)
  extraction = (/ 36.0d0, 64.0d0, 42.0d0, 24.0d0, 32.0d0 /)
  climate_stress = (/ 0.04d0, 0.04d0, 0.22d0, 0.03d0, 0.08d0 /)
  years = (/ 25, 25, 25, 25, 25 /)
  minimum_stock = (/ 250.0d0, 250.0d0, 250.0d0, 250.0d0, 250.0d0 /)

  print '(A)', 'key final_stock minimum_observed_stock minimum_resilience_margin threshold_breach'

  do i = 1, n
    call evaluate_resource(initial_stock(i), growth_rate(i), capacity(i), extraction(i), &
      climate_stress(i), years(i), minimum_stock(i), final_stock(i), min_stock(i), min_margin(i))
    breach = min_stock(i) < minimum_stock(i)
    print '(A,1X,F10.3,1X,F10.3,1X,F10.3,1X,L1)', trim(keys(i)), &
      final_stock(i), min_stock(i), min_margin(i), breach
  end do

contains

  subroutine evaluate_resource(initial, growth, carrying_capacity, extraction_rate, stress, &
      n_years, threshold_stock, final_value, min_value, min_margin_value)
    implicit none
    real(8), intent(in) :: initial, growth, carrying_capacity, extraction_rate, stress
    integer, intent(in) :: n_years
    real(8), intent(in) :: threshold_stock
    real(8), intent(out) :: final_value, min_value, min_margin_value
    integer :: year
    real(8) :: stock, effective_growth, regeneration

    stock = initial
    effective_growth = growth * (1.0d0 - stress)
    min_value = stock
    min_margin_value = stock - threshold_stock

    do year = 1, n_years
      regeneration = effective_growth * stock * (1.0d0 - stock / carrying_capacity)
      stock = max(0.0d0, stock + regeneration - extraction_rate)
      min_value = min(min_value, stock)
      min_margin_value = min(min_margin_value, stock - threshold_stock)
    end do

    final_value = stock
  end subroutine evaluate_resource

end program sustainability_scenario_summary
