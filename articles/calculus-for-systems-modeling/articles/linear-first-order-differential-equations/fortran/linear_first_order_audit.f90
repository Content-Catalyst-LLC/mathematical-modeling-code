program linear_first_order_audit
  implicit none
  real(8) :: y0, y, input_rate, loss_rate, dt, eq, t, a
  integer :: n, steps
  y0 = 20.0d0; y = 20.0d0; input_rate = 12.0d0; loss_rate = 0.4d0; dt = 0.1d0; steps = 100
  eq = input_rate / loss_rate
  print '(A)', 'scenario time analytical_state euler_state absolute_error input_rate loss_rate equilibrium initial_state method'
  do n = 0, steps
    t = n * dt
    a = eq + (y0 - eq) * exp(-loss_rate * t)
    print '(A,9F12.6,1X,A)', 'input_loss_balance', t, a, y, abs(a-y), input_rate, loss_rate, eq, y0, 0.0d0, 'analytical_vs_euler'
    y = y + dt * (input_rate - loss_rate*y)
  end do
end program
