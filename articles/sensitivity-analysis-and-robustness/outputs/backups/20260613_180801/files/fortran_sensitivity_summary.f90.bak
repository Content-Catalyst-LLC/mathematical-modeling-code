program sensitivity_summary
  implicit none

  integer, parameter :: n = 5
  integer :: i
  character(len=32) :: names(n)
  real(8) :: baseline(n), low(n), high(n)
  real(8) :: base_output, low_output, high_output, width

  names = (/ 'initial_stock                  ', 'growth_rate                    ', 'carrying_capacity              ', 'extraction_rate                ', 'shock_intensity                ' /)
  baseline = (/80.0d0, 0.08d0, 120.0d0, 0.12d0, 0.03d0/)
  low = (/72.0d0, 0.04d0, 100.0d0, 0.08d0, 0.0d0/)
  high = (/88.0d0, 0.12d0, 140.0d0, 0.18d0, 0.08d0/)

  base_output = projection(baseline(1), baseline(2), baseline(3), baseline(4), baseline(5))

  print '(A)', 'parameter low_output baseline_output high_output range_width'

  do i = 1, n
    if (i == 1) then
      low_output = projection(low(i), baseline(2), baseline(3), baseline(4), baseline(5))
      high_output = projection(high(i), baseline(2), baseline(3), baseline(4), baseline(5))
    else if (i == 2) then
      low_output = projection(baseline(1), low(i), baseline(3), baseline(4), baseline(5))
      high_output = projection(baseline(1), high(i), baseline(3), baseline(4), baseline(5))
    else if (i == 3) then
      low_output = projection(baseline(1), baseline(2), low(i), baseline(4), baseline(5))
      high_output = projection(baseline(1), baseline(2), high(i), baseline(4), baseline(5))
    else if (i == 4) then
      low_output = projection(baseline(1), baseline(2), baseline(3), low(i), baseline(5))
      high_output = projection(baseline(1), baseline(2), baseline(3), high(i), baseline(5))
    else
      low_output = projection(baseline(1), baseline(2), baseline(3), baseline(4), low(i))
      high_output = projection(baseline(1), baseline(2), baseline(3), baseline(4), high(i))
    end if

    width = abs(high_output - low_output)
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4)', trim(names(i)), low_output, base_output, high_output, width
  end do

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

end program sensitivity_summary
