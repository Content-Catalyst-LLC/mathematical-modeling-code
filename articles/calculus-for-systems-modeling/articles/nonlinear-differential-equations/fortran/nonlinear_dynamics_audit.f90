program nonlinear_dynamics_audit
  implicit none
  call simulate_logistic()
  call simulate_threshold()
contains
  real(8) function logistic_rate(x, growth, carrying)
    real(8), intent(in) :: x, growth, carrying
    logistic_rate = growth*x*(1.0d0 - x/carrying)
  end function
  real(8) function bistable_rate(x, threshold)
    real(8), intent(in) :: x, threshold
    bistable_rate = x*(1.0d0-x)*(x-threshold)
  end function
  subroutine simulate_logistic()
    real(8) :: x, dt, growth, carrying, t, r
    integer :: n
    x = 10.0d0; dt = 0.05d0; growth = 0.6d0; carrying = 100.0d0
    do n = 0, 300
      t = n*dt
      r = logistic_rate(x, growth, carrying)
      print '(A,6F12.6,1X,A)', 'logistic_growth', t, x, r, growth, carrying, 0.0d0, 'explicit_euler'
      x = x + dt*r
    end do
  end subroutine
  subroutine simulate_threshold()
    real(8) :: x, dt, threshold, t, r
    integer :: n
    x = 0.35d0; dt = 0.05d0; threshold = 0.4d0
    do n = 0, 300
      t = n*dt
      r = bistable_rate(x, threshold)
      print '(A,6F12.6,1X,A)', 'bistable_threshold', t, x, r, threshold, 0.0d0, 0.0d0, 'explicit_euler'
      x = x + dt*r
    end do
  end subroutine
end program
