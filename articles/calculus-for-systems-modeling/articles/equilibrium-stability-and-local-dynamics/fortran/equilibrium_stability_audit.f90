program equilibrium_stability_audit
  implicit none
  call print_logistic(0.0d0)
  call print_logistic(100.0d0)
  call print_bistable(0.0d0)
  call print_bistable(0.4d0)
  call print_bistable(1.0d0)
contains
  real(8) function logistic_derivative(x, growth, carrying)
    real(8), intent(in) :: x, growth, carrying
    logistic_derivative = growth*(1.0d0 - 2.0d0*x/carrying)
  end function
  real(8) function bistable_rate(x, threshold)
    real(8), intent(in) :: x, threshold
    bistable_rate = x*(1.0d0-x)*(x-threshold)
  end function
  real(8) function numerical_derivative(x, threshold)
    real(8), intent(in) :: x, threshold
    real(8) :: h
    h = 1.0d-5
    numerical_derivative = (bistable_rate(x+h, threshold) - bistable_rate(x-h, threshold))/(2.0d0*h)
  end function
  character(len=32) function classify(d)
    real(8), intent(in) :: d
    if (d < -1.0d-8) then
      classify = 'locally_stable'
    else if (d > 1.0d-8) then
      classify = 'locally_unstable'
    else
      classify = 'inconclusive_by_linearization'
    end if
  end function
  subroutine print_logistic(eq)
    real(8), intent(in) :: eq
    real(8) :: d
    d = logistic_derivative(eq, 0.6d0, 100.0d0)
    print '(A,F12.6,1X,F12.6,1X,A)', 'logistic_growth', eq, d, trim(classify(d))
  end subroutine
  subroutine print_bistable(eq)
    real(8), intent(in) :: eq
    real(8) :: d
    d = numerical_derivative(eq, 0.4d0)
    print '(A,F12.6,1X,F12.6,1X,A)', 'bistable_threshold', eq, d, trim(classify(d))
  end subroutine
end program
