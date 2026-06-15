program fundamental_theorem_audit
  implicit none
  real(8), dimension(9) :: times
  real(8) :: accumulated_rate, endpoint_difference, residual, dt
  integer :: i
  times = (/0.0d0,0.25d0,0.5d0,0.75d0,1.0d0,1.25d0,1.5d0,1.75d0,2.0d0/)
  accumulated_rate = 0.0d0

  do i=1,8
    dt = times(i+1) - times(i)
    accumulated_rate = accumulated_rate + 0.5d0 * (rate_value(times(i)) + rate_value(times(i+1))) * dt
  end do

  endpoint_difference = state_value(times(9)) - state_value(times(1))
  residual = endpoint_difference - accumulated_rate

  print '(A)', 'interval_start interval_end endpoint_difference accumulated_rate residual'
  print '(F8.3,1X,F8.3,1X,F14.6,1X,F14.6,1X,F14.6)', times(1), times(9), endpoint_difference, accumulated_rate, residual

contains
  real(8) function state_value(t)
    real(8), intent(in) :: t
    state_value = 50.0d0 + 2.0d0*t + 3.0d0*sin(t)
  end function

  real(8) function rate_value(t)
    real(8), intent(in) :: t
    rate_value = 2.0d0 + 3.0d0*cos(t)
  end function
end program
