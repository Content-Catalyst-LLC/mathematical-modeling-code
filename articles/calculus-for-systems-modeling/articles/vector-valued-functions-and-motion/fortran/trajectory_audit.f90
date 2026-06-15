program trajectory_audit
  implicit none
  real(8), parameter :: pi = 3.14159265358979323846d0
  print '(A)', 'scenario time_step point_count approximate_arc_length displacement_magnitude path_efficiency average_speed maximum_speed domain warning'
  call audit(1.0d0, 'coarse_time_step')
  call audit(0.5d0, 'medium_time_step')
  call audit(0.25d0, 'fine_time_step')
contains
  subroutine position(t, x, y)
    real(8), intent(in) :: t
    real(8), intent(out) :: x, y
    x = t
    y = sin(t)
  end subroutine

  real(8) function distance_between(x1,y1,x2,y2)
    real(8), intent(in) :: x1,y1,x2,y2
    distance_between = sqrt((x2-x1)**2 + (y2-y1)**2)
  end function

  subroutine audit(step, scenario)
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: i, count
    real(8) :: first_x, first_y, prev_x, prev_y, x, y, seg, speed, arc, speed_sum, speed_max, disp, eff
    character(len=32) :: warning
    count = int((2.0d0*pi)/step) + 1
    call position(0.0d0, first_x, first_y)
    prev_x = first_x
    prev_y = first_y
    arc = 0.0d0
    speed_sum = 0.0d0
    speed_max = 0.0d0
    do i = 1, count-1
      call position(i*step, x, y)
      seg = distance_between(prev_x, prev_y, x, y)
      speed = seg / step
      arc = arc + seg
      speed_sum = speed_sum + speed
      speed_max = max(speed_max, speed)
      prev_x = x
      prev_y = y
    end do
    disp = distance_between(first_x, first_y, prev_x, prev_y)
    eff = disp / max(arc, 1.0d-12)
    if (step > 0.5d0) then
      warning = 'coarse_time_step'
    else
      warning = 'synthetic_trajectory'
    end if
    print '(A,1X,F8.3,1X,I8,5F14.6,1X,A,1X,A)', trim(scenario), step, count, arc, disp, eff, speed_sum/(count-1), speed_max, 'trajectory', trim(warning)
  end subroutine
end program
