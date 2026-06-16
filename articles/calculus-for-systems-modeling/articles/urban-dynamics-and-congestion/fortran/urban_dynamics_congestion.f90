program urban_dynamics_congestion
  implicit none
  real(8) :: density, free_flow_speed, jam_density, flow, free_flow_time, volume, capacity, travel_time
  density = 35.0d0
  free_flow_speed = 60.0d0
  jam_density = 140.0d0
  flow = free_flow_speed * density * (1.0d0 - density / jam_density)
  free_flow_time = 20.0d0
  volume = 1800.0d0
  capacity = 2000.0d0
  travel_time = free_flow_time * (1.0d0 + 0.15d0 * (volume / capacity)**4)
  print '(A)', 'scenario flow travel_time'
  print '(A,1X,F12.6,1X,F12.6)', 'below_capacity_corridor', flow, travel_time
end program
