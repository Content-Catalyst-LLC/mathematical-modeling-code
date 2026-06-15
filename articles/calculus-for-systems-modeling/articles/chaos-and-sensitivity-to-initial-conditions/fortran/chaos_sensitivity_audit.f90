program chaos_sensitivity_audit
  implicit none
  integer :: step
  real(8) :: r, x_reference, x_perturbed, difference, log_difference
  r = 3.9d0
  x_reference = 0.2d0
  x_perturbed = 0.2d0 + 1.0d-8
  print '(A)', 'step x_reference x_perturbed absolute_difference log_difference'
  do step = 0, 100
    difference = abs(x_reference - x_perturbed)
    if (difference > 0.0d0) then
      log_difference = log(difference)
    else
      log_difference = 0.0d0
    end if
    print '(I6,4F18.10)', step, x_reference, x_perturbed, difference, log_difference
    x_reference = logistic_map(x_reference, r)
    x_perturbed = logistic_map(x_perturbed, r)
  end do
contains
  real(8) function logistic_map(x, r)
    real(8), intent(in) :: x, r
    logistic_map = r * x * (1.0d0 - x)
  end function
end program
