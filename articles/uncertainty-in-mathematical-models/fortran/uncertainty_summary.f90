program uncertainty_summary
  implicit none

  integer, parameter :: n = 1000
  integer :: i, threshold_count
  real(8) :: outputs(n), values(5), y
  real(8) :: mean_output, threshold_probability

  call random_seed()
  threshold_count = 0

  do i = 1, n
    call random_number(values)
    values(1) = 72.0d0 + values(1) * (88.0d0 - 72.0d0)
    values(2) = 0.04d0 + values(2) * (0.12d0 - 0.04d0)
    values(3) = 100.0d0 + values(3) * (140.0d0 - 100.0d0)
    values(4) = 0.08d0 + values(4) * (0.18d0 - 0.08d0)
    values(5) = 0.00d0 + values(5) * (0.08d0 - 0.00d0)

    y = projection(values(1), values(2), values(3), values(4), values(5))
    outputs(i) = y
    if (y < 45.0d0) threshold_count = threshold_count + 1
  end do

  mean_output = sum(outputs) / real(n, 8)
  threshold_probability = real(threshold_count, 8) / real(n, 8)

  print '(A)', 'mean threshold_probability min max'
  print '(F10.4,1X,F10.4,1X,F10.4,1X,F10.4)', mean_output, threshold_probability, minval(outputs), maxval(outputs)

contains

  real(8) function projection(initial_stock, growth_rate, carrying_capacity, extraction_rate, shock_intensity)
    implicit none
    real(8), intent(in) :: initial_stock, growth_rate, carrying_capacity, extraction_rate, shock_intensity
    integer :: year
    real(8) :: stock, growth, extraction, shock

    stock = initial_stock
    do year = 1, 10
      growth = growth_rate * stock * (1.0d0 - stock / carrying_capacity)
      extraction = extraction_rate * stock
      shock = shock_intensity * stock
      stock = max(0.0d0, stock + growth - extraction - shock)
    end do
    projection = stock
  end function projection

end program uncertainty_summary
