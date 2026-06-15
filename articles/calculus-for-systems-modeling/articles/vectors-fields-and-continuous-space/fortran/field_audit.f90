program field_audit
  implicit none
  print '(A)', 'scenario grid_step point_count scalar_average scalar_minimum scalar_maximum vector_magnitude_average vector_magnitude_maximum domain warning'
  call audit(1.0d0, 'coarse_grid')
  call audit(0.5d0, 'medium_grid')
  call audit(0.25d0, 'fine_grid')
contains
  real(8) function scalar_field(x,y)
    real(8), intent(in) :: x, y
    scalar_field = 20.0d0 + 2.0d0 * sin(x) + 0.5d0 * y * y
  end function

  real(8) function vector_magnitude(vx,vy)
    real(8), intent(in) :: vx, vy
    vector_magnitude = sqrt(vx*vx + vy*vy)
  end function

  subroutine audit(step, scenario)
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: i, j, n, count
    real(8) :: x, y, s, vx, vy, mag, scalar_sum, scalar_min, scalar_max, mag_sum, mag_max
    character(len=60) :: warning
    n = int(6.0d0 / step)
    count = 0
    scalar_sum = 0.0d0
    scalar_min = 1.0d99
    scalar_max = -1.0d99
    mag_sum = 0.0d0
    mag_max = 0.0d0
    do i = 0, n
      x = -3.0d0 + i * step
      do j = 0, n
        y = -3.0d0 + j * step
        s = scalar_field(x,y)
        vx = -y
        vy = x
        mag = vector_magnitude(vx,vy)
        count = count + 1
        scalar_sum = scalar_sum + s
        scalar_min = min(scalar_min, s)
        scalar_max = max(scalar_max, s)
        mag_sum = mag_sum + mag
        mag_max = max(mag_max, mag)
      end do
    end do
    if (step > 0.75d0) then
      warning = 'coarse_grid'
    else
      warning = 'synthetic_field_audit'
    end if
    print '(A,1X,F8.3,1X,I8,5F14.6,1X,A,1X,A)', trim(scenario), step, count, scalar_sum/count, scalar_min, scalar_max, mag_sum/count, mag_max, 'square_domain', trim(warning)
  end subroutine
end program
