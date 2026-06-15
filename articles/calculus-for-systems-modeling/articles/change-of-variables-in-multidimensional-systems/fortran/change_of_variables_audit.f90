program change_of_variables_audit
  implicit none
  real(8), parameter :: pi = 3.14159265358979323846d0
  print '(A)', 'scenario radius radial_step angular_step polar_total cartesian_total absolute_difference relative_difference jacobian_rule warning'
  call audit(3.0d0, 0.5d0, pi / 24.0d0, 'medium_polar_grid')
  call audit(3.0d0, 0.25d0, pi / 48.0d0, 'fine_polar_grid')
  call audit(3.0d0, 0.125d0, pi / 96.0d0, 'very_fine_polar_grid')
contains
  real(8) function exposure_cartesian(x,y)
    real(8), intent(in) :: x, y
    real(8) :: r
    r = sqrt(x*x + y*y)
    exposure_cartesian = 20.0d0 * exp(-0.4d0 * r)
  end function

  real(8) function exposure_polar(r,theta)
    real(8), intent(in) :: r, theta
    exposure_polar = 20.0d0 * exp(-0.4d0 * r)
  end function

  real(8) function polar_total(radius, dr, dtheta)
    real(8), intent(in) :: radius, dr, dtheta
    real(8) :: r, theta
    polar_total = 0.0d0
    r = dr / 2.0d0
    do while (r < radius)
      theta = dtheta / 2.0d0
      do while (theta < 2.0d0 * pi)
        polar_total = polar_total + exposure_polar(r, theta) * r * dr * dtheta
        theta = theta + dtheta
      end do
      r = r + dr
    end do
  end function

  real(8) function cartesian_grid_total(radius, step)
    real(8), intent(in) :: radius, step
    integer :: i, j, n
    real(8) :: x, y
    n = int((2.0d0 * radius) / step)
    cartesian_grid_total = 0.0d0
    do i=0,n
      x = -radius + i * step
      do j=0,n
        y = -radius + j * step
        if (x*x + y*y <= radius*radius) then
          cartesian_grid_total = cartesian_grid_total + exposure_cartesian(x,y) * step * step
        end if
      end do
    end do
  end function

  subroutine audit(radius, dr, dtheta, scenario)
    real(8), intent(in) :: radius, dr, dtheta
    character(len=*), intent(in) :: scenario
    real(8) :: p, c, diff, rel
    p = polar_total(radius, dr, dtheta)
    c = cartesian_grid_total(radius, dr)
    diff = abs(p - c)
    rel = diff / max(abs(p), 1.0d-12)
    print '(A,8F14.6,1X,A,1X,A)', trim(scenario), radius, dr, dtheta, p, c, diff, rel, 0.0d0, 'jacobian_r', 'review_domain_resolution'
  end subroutine
end program
