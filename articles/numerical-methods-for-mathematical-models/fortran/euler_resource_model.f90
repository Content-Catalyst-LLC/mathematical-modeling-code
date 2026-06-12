program euler_resource_model
  implicit none

  real(8), parameter :: growth_rate = 0.18d0
  real(8), parameter :: carrying_capacity = 100.0d0
  real(8), parameter :: extraction = 6.0d0
  real(8), parameter :: horizon = 50.0d0
  real(8) :: step_sizes(4)
  real(8) :: stock, final_stock, reference
  integer :: i

  step_sizes = (/1.0d0, 0.5d0, 0.25d0, 0.1d0/)
  reference = run_euler(0.1d0)

  print '(A)', 'step_size final_stock difference_from_finest'

  do i = 1, 4
    final_stock = run_euler(step_sizes(i))
    print '(F6.3,1X,F10.4,1X,F10.4)', step_sizes(i), final_stock, abs(final_stock - reference)
  end do

contains

  real(8) function derivative(stock)
    real(8), intent(in) :: stock
    derivative = growth_rate * stock * (1.0d0 - stock / carrying_capacity) - extraction
  end function derivative

  real(8) function run_euler(h)
    real(8), intent(in) :: h
    integer :: steps, j
    real(8) :: s

    steps = nint(horizon / h)
    s = 70.0d0

    do j = 1, steps
      s = s + h * derivative(s)
      s = max(0.0d0, s)
    end do

    run_euler = s
  end function run_euler

end program euler_resource_model
