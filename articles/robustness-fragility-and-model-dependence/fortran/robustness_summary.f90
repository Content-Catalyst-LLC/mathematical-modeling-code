program robustness_summary
  implicit none

  integer, parameter :: n = 6
  character(len=32) :: keys(n), forms(n), scenario_names(n)
  real(8) :: multipliers(n), shocks(n), outputs(n)
  integer :: i

  keys = (/ 'linear_baseline               ', 'linear_stress                 ', 'dynamic_baseline              ', 'dynamic_stress                ', 'threshold_baseline            ', 'threshold_stress              ' /)
  forms = (/ 'linear_decline                ', 'linear_decline                ', 'logistic_recovery             ', 'logistic_recovery             ', 'threshold_shift               ', 'threshold_shift               ' /)
  scenario_names = (/ 'baseline                      ', 'stress                        ', 'baseline                      ', 'stress                        ', 'baseline                      ', 'stress                        ' /)
  multipliers = (/ 1.0d0, 1.25d0, 1.0d0, 1.25d0, 1.0d0, 1.25d0 /)
  shocks = (/ 0.0d0, 0.05d0, 0.0d0, 0.05d0, 0.0d0, 0.05d0 /)

  print '(A)', 'key model_form scenario projected_stock below_threshold'

  do i = 1, n
    outputs(i) = simulate(trim(forms(i)), multipliers(i), shocks(i))
    print '(A,1X,A,1X,A,1X,F10.4,1X,L1)', trim(keys(i)), trim(forms(i)), trim(scenario_names(i)), outputs(i), outputs(i) < 45.0d0
  end do

  print '(A,F10.4)', 'robustness_spread ', maxval(outputs) - minval(outputs)

contains

  real(8) function simulate(form, extraction_multiplier, shock)
    implicit none
    character(len=*), intent(in) :: form
    real(8), intent(in) :: extraction_multiplier, shock
    integer :: year
    real(8) :: stock, carrying_capacity, growth_rate, extraction_rate
    real(8) :: fixed_loss, critical_threshold, growth, extraction

    stock = 80.0d0
    carrying_capacity = 120.0d0
    growth_rate = 0.08d0
    extraction_rate = 0.12d0 * extraction_multiplier
    fixed_loss = 5.8d0 * extraction_multiplier
    critical_threshold = 55.0d0

    do year = 1, 10
      if (form == 'linear_decline') then
        stock = max(0.0d0, stock - fixed_loss - shock * stock)
      else if (form == 'logistic_recovery') then
        growth = growth_rate * stock * (1.0d0 - stock / carrying_capacity)
        extraction = extraction_rate * stock
        stock = max(0.0d0, stock + growth - extraction - shock * stock)
      else if (form == 'threshold_shift') then
        if (stock < critical_threshold) then
          stock = max(0.0d0, stock - 1.6d0 * extraction_rate * stock - shock * stock)
        else
          stock = max(0.0d0, stock - extraction_rate * stock - shock * stock)
        end if
      end if
    end do

    simulate = stock
  end function simulate

end program robustness_summary
