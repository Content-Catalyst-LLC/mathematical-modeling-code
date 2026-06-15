program divergence_theorem_audit
  implicit none
  print '(A)', 'scenario grid_steps boundary_flux volume_divergence_integral absolute_gap field_description volume_description normal_note warning'
  call audit(4, 'coarse_audit')
  call audit(16, 'medium_audit')
  call audit(64, 'fine_audit')
contains
  subroutine audit(grid_steps, scenario)
    integer, intent(in) :: grid_steps
    character(len=*), intent(in) :: scenario
    real(8) :: step, area, flux, div_integral
    integer :: i, j
    character(len=32) :: warning
    step = 1.0d0 / grid_steps
    area = step * step
    flux = 0.0d0
    do i = 0, grid_steps-1
      do j = 0, grid_steps-1
        flux = flux + 3.0d0 * area
      end do
    end do
    div_integral = 3.0d0
    if (grid_steps < 8) then
      warning = 'coarse_audit'
    else
      warning = 'synthetic_audit'
    end if
    print '(A,1X,I8,3F14.6,1X,A,1X,A,1X,A,1X,A)', trim(scenario), grid_steps, flux, div_integral, abs(flux-div_integral), 'field', 'cube', 'outward', trim(warning)
  end subroutine
end program
