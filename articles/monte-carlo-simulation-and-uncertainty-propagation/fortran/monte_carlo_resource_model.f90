program monte_carlo_resource_model
  implicit none

  integer, parameter :: replications = 1000
  integer :: i, step, depleted
  real(8) :: stock, growth_rate, extraction, shock_probability
  real(8) :: growth, shock, u, total_final_stock
  real(8), parameter :: shock_fraction = 0.12d0
  real(8), parameter :: capacity = 100.0d0

  call random_seed()
  total_final_stock = 0.0d0
  depleted = 0

  do i = 1, replications
    call random_number(u)
    stock = 65.0d0 + u * (75.0d0 - 65.0d0)

    call random_number(u)
    growth_rate = 0.14d0 + u * (0.22d0 - 0.14d0)

    call random_number(u)
    extraction = 5.0d0 + u * (8.0d0 - 5.0d0)

    call random_number(u)
    shock_probability = 0.02d0 + u * (0.08d0 - 0.02d0)

    do step = 1, 50
      growth = growth_rate * stock * (1.0d0 - stock / capacity)
      call random_number(u)
      if (u < shock_probability) then
        shock = stock * shock_fraction
      else
        shock = 0.0d0
      end if
      stock = max(0.0d0, stock + growth - extraction - shock)
    end do

    total_final_stock = total_final_stock + stock
    if (stock <= 10.0d0) depleted = depleted + 1
  end do

  print '(A)', 'replications mean_final_stock depletion_probability'
  print '(I0,1X,F10.4,1X,F10.4)', replications, total_final_stock / replications, real(depleted, 8) / replications
end program monte_carlo_resource_model
