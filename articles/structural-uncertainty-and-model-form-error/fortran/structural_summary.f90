program structural_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: forms(n)
  real(8) :: outputs(n)
  integer :: i

  forms = (/ 'linear_decline                 ', 'proportional_decline           ', 'logistic_recovery              ', 'threshold_shift                ' /)

  do i = 1, n
    outputs(i) = simulate_model(trim(forms(i)))
  end do

  print '(A)', 'model_form projected_stock below_threshold'
  do i = 1, n
    print '(A,1X,F10.4,1X,L1)', trim(forms(i)), outputs(i), outputs(i) < 45.0d0
  end do

  print '(A,F10.4)', 'structural_spread ', maxval(outputs) - minval(outputs)

contains

  real(8) function simulate_model(form_key)
    implicit none
    character(len=*), intent(in) :: form_key
    integer :: year
    real(8) :: stock, carrying_capacity, extraction_rate, growth_rate
    real(8) :: fixed_loss, critical_threshold, growth, extraction

    stock = 80.0d0
    carrying_capacity = 120.0d0
    extraction_rate = 0.12d0
    growth_rate = 0.08d0
    fixed_loss = 5.8d0
    critical_threshold = 55.0d0

    do year = 1, 10
      if (form_key == 'linear_decline') then
        stock = max(0.0d0, stock - fixed_loss)
      else if (form_key == 'proportional_decline') then
        stock = max(0.0d0, stock - extraction_rate * stock)
      else if (form_key == 'logistic_recovery') then
        growth = growth_rate * stock * (1.0d0 - stock / carrying_capacity)
        extraction = extraction_rate * stock
        stock = max(0.0d0, stock + growth - extraction)
      else if (form_key == 'threshold_shift') then
        if (stock < critical_threshold) then
          stock = max(0.0d0, stock - 1.6d0 * extraction_rate * stock)
        else
          stock = max(0.0d0, stock - extraction_rate * stock)
        end if
      end if
    end do

    simulate_model = stock
  end function simulate_model

end program structural_summary
