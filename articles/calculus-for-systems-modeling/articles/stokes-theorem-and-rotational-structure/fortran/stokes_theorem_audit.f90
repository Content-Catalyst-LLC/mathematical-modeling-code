program stokes_theorem_audit
  implicit none
  print '(A)', 'scenario radius boundary_segments radial_steps boundary_circulation surface_curl_flux absolute_gap field_description surface_description orientation_note warning'
  call audit(1.0d0, 32, 8, 'coarse_audit')
  call audit(1.0d0, 128, 32, 'medium_audit')
  call audit(1.0d0, 512, 128, 'fine_audit')
contains
  subroutine audit(radius, segments, radial_steps, scenario)
    real(8), intent(in) :: radius
    integer, intent(in) :: segments, radial_steps
    character(len=*), intent(in) :: scenario
    integer :: i
    real(8) :: pi, theta0, theta1, x0, y0, x1, y1, xm, ym, dx, dy, circulation, curl_flux
    real(8) :: r0, r1, ring_area
    character(len=32) :: warning
    pi = 4.0d0*atan(1.0d0)
    circulation = 0.0d0
    do i = 0, segments-1
      theta0 = 2.0d0*pi*i/segments
      theta1 = 2.0d0*pi*(i+1)/segments
      x0 = radius*cos(theta0); y0 = radius*sin(theta0)
      x1 = radius*cos(theta1); y1 = radius*sin(theta1)
      xm = 0.5d0*(x0+x1); ym = 0.5d0*(y0+y1)
      dx = x1-x0; dy = y1-y0
      circulation = circulation + (-ym)*dx + xm*dy
    end do
    curl_flux = 0.0d0
    do i = 0, radial_steps-1
      r0 = radius*i/radial_steps
      r1 = radius*(i+1)/radial_steps
      ring_area = pi*(r1*r1 - r0*r0)
      curl_flux = curl_flux + 2.0d0*ring_area
    end do
    if (segments < 64 .or. radial_steps < 16) then
      warning = 'coarse_audit'
    else
      warning = 'synthetic_audit'
    end if
    print '(A,1X,F8.3,2I8,3F14.6,1X,A,1X,A,1X,A,1X,A)', trim(scenario), radius, segments, radial_steps, circulation, curl_flux, abs(circulation-curl_flux), 'field', 'disk', 'ccw_up', trim(warning)
  end subroutine
end program
