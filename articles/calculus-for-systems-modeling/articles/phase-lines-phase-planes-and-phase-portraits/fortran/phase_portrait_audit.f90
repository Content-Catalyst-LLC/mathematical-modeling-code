program phase_portrait_audit
  implicit none
  real(8) :: alpha, beta, delta, gamma, x, y, dxdt, dydt, speed
  integer :: xi, yi
  alpha = 0.7d0; beta = 0.05d0; delta = 0.02d0; gamma = 0.5d0
  print '(A)', 'x y dxdt dydt x_nullcline_residual y_nullcline_residual speed'
  do xi = 0, 60, 5
    do yi = 0, 30, 3
      x = dble(xi); y = dble(yi)
      dxdt = alpha*x - beta*x*y
      dydt = delta*x*y - gamma*y
      speed = sqrt(dxdt*dxdt + dydt*dydt)
      print '(7F12.6)', x, y, dxdt, dydt, dxdt, dydt, speed
    end do
  end do
end program
