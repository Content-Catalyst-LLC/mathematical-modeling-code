program advection_diffusion_audit
  implicit none
  integer, parameter :: grid_points = 61, steps = 120
  integer :: step, i
  real(8) :: diffusivity, velocity, dx, dt, d_ratio, t_ratio, total_mass, max_value, min_value
  real(8), dimension(grid_points) :: field, updated

  diffusivity = 0.08d0
  velocity = 0.4d0
  dx = 1.0d0
  dt = 0.2d0
  d_ratio = diffusivity * dt / (dx * dx)
  t_ratio = velocity * dt / dx
  field = 0.0d0
  field((grid_points + 1) / 2) = 1.0d0

  print '(A)', 'step time center_value total_mass max_value min_value diffusion_ratio transport_ratio'
  do step = 0, steps
    total_mass = sum(field) * dx
    max_value = maxval(field)
    min_value = minval(field)
    print '(I6,7F14.6)', step, dble(step)*dt, field((grid_points + 1) / 2), total_mass, max_value, min_value, d_ratio, t_ratio

    updated = field
    do i = 2, grid_points - 1
      updated(i) = field(i) + d_ratio * (field(i + 1) - 2.0d0 * field(i) + field(i - 1)) - t_ratio * (field(i) - field(i - 1))
    end do
    updated(1) = 0.0d0
    updated(grid_points) = 0.0d0
    field = updated
  end do
end program
