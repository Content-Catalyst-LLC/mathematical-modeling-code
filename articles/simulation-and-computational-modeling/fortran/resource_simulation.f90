program resource_simulation
  implicit none

  integer, parameter :: steps = 20
  real(8) :: stock
  real(8), parameter :: growth_rate = 0.18d0
  real(8), parameter :: capacity = 100.0d0
  real(8), parameter :: extraction = 6.0d0
  real(8) :: growth
  integer :: t

  stock = 70.0d0

  print '(A)', 'step resource_stock'

  do t = 0, steps
    print '(I0,1X,F10.4)', t, stock
    growth = growth_rate * stock * (1.0d0 - stock / capacity)
    stock = max(0.0d0, stock + growth - extraction)
  end do
end program resource_simulation
