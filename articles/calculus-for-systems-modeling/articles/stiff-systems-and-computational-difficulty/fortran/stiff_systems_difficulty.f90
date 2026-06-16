program stiff_systems_difficulty
  implicit none
  integer :: i
  real(8), dimension(4) :: hs
  real(8) :: y0, lambda, stop_time, exact_final, explicit_final, implicit_final, h, eamp, iamp

  y0 = 1.0d0
  lambda = -50.0d0
  stop_time = 1.0d0
  hs = (/0.1d0, 0.05d0, 0.025d0, 0.01d0/)
  exact_final = y0 * exp(lambda * stop_time)

  print '(A)', 'step_size eigenvalue method amplification_factor final_value exact_final_value absolute_error'
  do i = 1, 4
    h = hs(i)
    explicit_final = explicit_value(y0, lambda, h, stop_time)
    implicit_final = implicit_value(y0, lambda, h, stop_time)
    eamp = abs(1.0d0 + h * lambda)
    iamp = abs(1.0d0 / (1.0d0 - h * lambda))
    print '(F10.4,F12.4,A18,4F18.10)', h, lambda, ' explicit_euler ', eamp, explicit_final, exact_final, abs(explicit_final - exact_final)
    print '(F10.4,F12.4,A18,4F18.10)', h, lambda, ' implicit_euler ', iamp, implicit_final, exact_final, abs(implicit_final - exact_final)
  end do

contains
  real(8) function explicit_value(y0, lambda, h, stop_time)
    real(8), intent(in) :: y0, lambda, h, stop_time
    integer :: step, steps
    real(8) :: y, amp
    steps = nint(stop_time / h)
    amp = 1.0d0 + h * lambda
    y = y0
    do step = 1, steps
      y = amp * y
    end do
    explicit_value = y
  end function

  real(8) function implicit_value(y0, lambda, h, stop_time)
    real(8), intent(in) :: y0, lambda, h, stop_time
    integer :: step, steps
    real(8) :: y, amp
    steps = nint(stop_time / h)
    amp = 1.0d0 / (1.0d0 - h * lambda)
    y = y0
    do step = 1, steps
      y = amp * y
    end do
    implicit_value = y
  end function
end program
