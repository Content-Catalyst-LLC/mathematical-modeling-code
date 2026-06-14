program functional_forms
  implicit none
  real(8) :: x

  x = 10.0d0

  print '(A)', 'model final_value'
  print '(A,1X,F10.6)', 'linear_growth', linear_model(x)
  print '(A,1X,F10.6)', 'exponential_growth', exponential_model(x)
  print '(A,1X,F10.6)', 'logistic_growth', logistic_model(x)
  print '(A,1X,F10.6)', 'threshold_response', threshold_model(x)

contains

  real(8) function linear_model(x)
    real(8), intent(in) :: x
    linear_model = 10.0d0 + 2.0d0 * x
  end function linear_model

  real(8) function exponential_model(x)
    real(8), intent(in) :: x
    exponential_model = 10.0d0 * exp(0.18d0 * x)
  end function exponential_model

  real(8) function logistic_model(x)
    real(8), intent(in) :: x
    logistic_model = 100.0d0 / (1.0d0 + exp(-0.75d0 * (x - 5.0d0)))
  end function logistic_model

  real(8) function threshold_model(x)
    real(8), intent(in) :: x
    if (x < 5.0d0) then
      threshold_model = 20.0d0
    else
      threshold_model = 80.0d0
    end if
  end function threshold_model

end program functional_forms
