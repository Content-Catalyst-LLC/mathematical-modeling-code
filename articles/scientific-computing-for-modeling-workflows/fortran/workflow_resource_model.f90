program workflow_resource_model
  implicit none

  integer, parameter :: steps = 50
  real(8) :: baseline, stress, recovery

  baseline = simulate(70.0d0, 0.18d0, 100.0d0, 6.0d0, steps)
  stress = simulate(70.0d0, 0.15d0, 100.0d0, 9.0d0, steps)
  recovery = simulate(70.0d0, 0.18d0, 100.0d0, 5.0d0, steps)

  print '(A)', 'scenario final_stock'
  print '(A,1X,F10.4)', 'baseline', baseline
  print '(A,1X,F10.4)', 'stress', stress
  print '(A,1X,F10.4)', 'recovery_policy', recovery

contains

  real(8) function simulate(initial_stock, growth_rate, capacity, extraction, n_steps)
    real(8), intent(in) :: initial_stock, growth_rate, capacity, extraction
    integer, intent(in) :: n_steps
    integer :: i
    real(8) :: stock, growth

    stock = initial_stock
    do i = 1, n_steps
      growth = growth_rate * stock * (1.0d0 - stock / capacity)
      stock = max(0.0d0, stock + growth - extraction)
    end do
    simulate = stock
  end function simulate

end program workflow_resource_model
