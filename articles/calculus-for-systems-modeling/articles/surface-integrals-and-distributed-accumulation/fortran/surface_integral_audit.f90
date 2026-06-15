program surface_integral_audit
  implicit none
  print '(A)', 'scenario grid_step patch_count approximate_surface_area scalar_surface_integral vector_flux_integral average_flux_density maximum_patch_area surface_description warning'
  call audit(1.0d0, 'coarse_surface_mesh')
  call audit(0.5d0, 'medium_surface_mesh')
  call audit(0.25d0, 'fine_surface_mesh')
contains
  real(8) function height(x,y)
    real(8), intent(in) :: x,y
    height = 0.1d0*x*x + 0.05d0*y*y
  end function

  real(8) function scalar_field(x,y,z)
    real(8), intent(in) :: x,y,z
    scalar_field = 1.0d0 + 0.2d0*z
  end function

  subroutine normal_area_vector(x,y,step,ax,ay,az)
    real(8), intent(in) :: x,y,step
    real(8), intent(out) :: ax,ay,az
    real(8) :: area
    area = step*step
    ax = -0.2d0*x*area
    ay = -0.1d0*y*area
    az = area
  end subroutine

  real(8) function norm3(x,y,z)
    real(8), intent(in) :: x,y,z
    norm3 = sqrt(x*x+y*y+z*z)
  end function

  subroutine audit(step, scenario)
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: i,j,n,count
    real(8) :: x,y,z,ax,ay,az,vx,vy,vz,patch_area,flux
    real(8) :: surface_area,scalar_total,flux_total,flux_density_sum,max_patch
    character(len=32) :: warning
    n = int(2.0d0 / step)
    count = 0
    surface_area = 0.0d0
    scalar_total = 0.0d0
    flux_total = 0.0d0
    flux_density_sum = 0.0d0
    max_patch = 0.0d0
    do i = 0, n-1
      x = -1.0d0 + i*step
      do j = 0, n-1
        y = -1.0d0 + j*step
        z = height(x,y)
        call normal_area_vector(x,y,step,ax,ay,az)
        vx = 0.1d0*x
        vy = 0.1d0*y
        vz = 1.0d0
        patch_area = norm3(ax,ay,az)
        flux = vx*ax + vy*ay + vz*az
        count = count + 1
        surface_area = surface_area + patch_area
        scalar_total = scalar_total + scalar_field(x,y,z) * patch_area
        flux_total = flux_total + flux
        flux_density_sum = flux_density_sum + flux / max(patch_area, 1.0d-12)
        max_patch = max(max_patch, patch_area)
      end do
    end do
    if (step > 0.5d0) then
      warning = 'coarse_mesh'
    else
      warning = 'synthetic_surface'
    end if
    print '(A,1X,F8.3,1X,I8,5F14.6,1X,A,1X,A)', trim(scenario), step, count, surface_area, scalar_total, flux_total, flux_density_sum/count, max_patch, 'surface', trim(warning)
  end subroutine
end program
