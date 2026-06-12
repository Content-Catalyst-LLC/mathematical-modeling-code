program spatial_distance_diagnostics
  implicit none

  integer, parameter :: n_demand = 4, n_service = 3
  real(8) :: dx(n_demand), dy(n_demand), demand_value(n_demand)
  real(8) :: sx(n_service), sy(n_service), service_value(n_service)
  real(8) :: d, nearest_distance, accessibility
  integer :: i, j, nearest_index

  dx = (/0.0d0, 2.0d0, 4.0d0, 6.0d0/)
  dy = (/0.0d0, 1.0d0, 2.5d0, 1.5d0/)
  demand_value = (/1200.0d0, 900.0d0, 1400.0d0, 700.0d0/)

  sx = (/1.0d0, 5.5d0, 3.0d0/)
  sy = (/0.5d0, 2.0d0, 4.0d0/)
  service_value = (/500.0d0, 650.0d0, 400.0d0/)

  print '(A)', 'demand_index nearest_service_index nearest_distance accessibility_score'

  do i = 1, n_demand
    nearest_distance = huge(1.0d0)
    nearest_index = -1
    accessibility = 0.0d0

    do j = 1, n_service
      d = sqrt((dx(i)-sx(j))**2 + (dy(i)-sy(j))**2)
      accessibility = accessibility + service_value(j) / (1.0d0 + d)

      if (d < nearest_distance) then
        nearest_distance = d
        nearest_index = j
      end if
    end do

    print '(I0,1X,I0,1X,F10.4,1X,F10.4)', i, nearest_index, nearest_distance, accessibility
  end do
end program spatial_distance_diagnostics
