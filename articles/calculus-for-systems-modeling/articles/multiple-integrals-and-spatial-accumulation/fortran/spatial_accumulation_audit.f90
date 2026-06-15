program spatial_accumulation_audit
  implicit none
  print '(A)', 'scenario cells cell_area total_area total_density area_average population_burden population_total population_average warning'
  call compute(1.0d0, 'coarse_grid')
  call compute(0.5d0, 'medium_grid')
  call compute(0.25d0, 'fine_grid')
contains
  real(8) function exposure_field(x,y)
    real(8), intent(in) :: x, y
    exposure_field = 10.0d0 + 2.0d0*x + 0.5d0*y*y
  end function

  real(8) function population_density(x,y)
    real(8), intent(in) :: x, y
    population_density = 100.0d0 + 10.0d0*y + 5.0d0*sin(x)
  end function

  logical function in_region(x,y)
    real(8), intent(in) :: x, y
    in_region = x*x + y*y <= 9.0d0
  end function

  subroutine compute(step, scenario)
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: i, j, n, cells
    real(8) :: x, y, cell_area, exposure, population, total_density, total_population, population_burden, total_area
    character(len=80) :: warning
    n = int(6.0d0 / step)
    cell_area = step * step
    cells = 0
    total_density = 0.0d0
    total_population = 0.0d0
    population_burden = 0.0d0
    do i = 0, n
      x = -3.0d0 + i * step
      do j = 0, n
        y = -3.0d0 + j * step
        if (in_region(x,y)) then
          exposure = exposure_field(x,y)
          population = population_density(x,y)
          cells = cells + 1
          total_density = total_density + exposure * cell_area
          total_population = total_population + population * cell_area
          population_burden = population_burden + exposure * population * cell_area
        end if
      end do
    end do
    total_area = cells * cell_area
    if (step > 0.5d0) then
      warning = 'coarse_grid'
    else
      warning = 'synthetic_grid_audit'
    end if
    print '(A,1X,I6,7F14.6,1X,A)', trim(scenario), cells, cell_area, total_area, total_density, total_density/total_area, population_burden, total_population, population_burden/total_population, trim(warning)
  end subroutine
end program
