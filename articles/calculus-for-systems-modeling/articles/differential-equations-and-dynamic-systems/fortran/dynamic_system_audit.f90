program dynamic_system_audit
  implicit none
  call simulate('exponential_growth', .false.)
  call simulate('logistic_growth', .true.)
contains
  real(8) function exp_rate(x,r)
    real(8), intent(in) :: x,r
    exp_rate = r*x
  end function
  real(8) function log_rate(x,r,k)
    real(8), intent(in) :: x,r,k
    log_rate = r*x*(1.0d0 - x/k)
  end function
  subroutine simulate(label, logistic)
    character(len=*), intent(in) :: label
    logical, intent(in) :: logistic
    real(8) :: x, r, k, dt, t, rate
    integer :: n, steps
    x = 10.0d0; r = 0.35d0; k = 100.0d0; dt = 0.1d0; steps = 100
    do n = 0, steps
      t = n*dt
      if (logistic) then
        rate = log_rate(x,r,k)
        print '(A,1X,A,5F12.6,1X,A)', trim(label), 'logistic', t, x, rate, r, k, 'explicit_euler'
      else
        rate = exp_rate(x,r)
        print '(A,1X,A,5F12.6,1X,A)', trim(label), 'exponential', t, x, rate, r, -1.0d0, 'explicit_euler'
      end if
      x = x + dt*rate
    end do
  end subroutine
end program
