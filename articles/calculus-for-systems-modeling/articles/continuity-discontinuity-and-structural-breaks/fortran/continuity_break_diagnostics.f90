program continuity_break_diagnostics
  implicit none

  integer, parameter :: n = 41
  real(8) :: xs(n), ys(n)
  real(8) :: left_slope, right_slope, slope_change, level_jump
  integer :: i

  do i = 1, n
    xs(i) = 0.25d0 * real(i - 1, 8)
    ys(i) = piecewise_system(xs(i))
  end do

  print '(A)', 'x y left_slope right_slope slope_change level_jump flag'

  do i = 1, n
    if (i == 1 .or. i == n) then
      print '(F8.4,1X,F10.4,1X,A)', xs(i), ys(i), 'NA NA NA NA ok'
    else
      left_slope = (ys(i) - ys(i - 1)) / (xs(i) - xs(i - 1))
      right_slope = (ys(i + 1) - ys(i)) / (xs(i + 1) - xs(i))
      slope_change = abs(right_slope - left_slope)
      level_jump = abs(ys(i) - ys(i - 1))
      print '(F8.4,1X,F10.4,1X,F10.4,1X,F10.4,1X,F10.4,1X,F10.4,1X,A)', &
        xs(i), ys(i), left_slope, right_slope, slope_change, level_jump, trim(classify(level_jump, slope_change))
    end if
  end do

contains

  real(8) function piecewise_system(x)
    real(8), intent(in) :: x
    if (x < 5.0d0) then
      piecewise_system = 2.0d0 + 0.5d0 * x
    else
      piecewise_system = 6.0d0 + 1.4d0 * (x - 5.0d0)
    end if
  end function piecewise_system

  character(len=32) function classify(level_jump, slope_change)
    real(8), intent(in) :: level_jump, slope_change
    if (level_jump > 1.0d0 .and. slope_change > 0.5d0) then
      classify = 'level_and_slope_break'
    else if (level_jump > 1.0d0) then
      classify = 'possible_jump'
    else if (slope_change > 0.5d0) then
      classify = 'possible_slope_break'
    else
      classify = 'ok'
    end if
  end function classify

end program continuity_break_diagnostics
