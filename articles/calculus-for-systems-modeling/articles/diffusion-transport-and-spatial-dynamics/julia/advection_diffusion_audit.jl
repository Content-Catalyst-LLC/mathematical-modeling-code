function initialize_field(grid_points)
    field = zeros(Float64, grid_points)
    field[cld(grid_points, 2)] = 1.0
    return field
end

function update_advection_diffusion(field, d_ratio, t_ratio)
    updated = copy(field)
    for i in 2:(length(field)-1)
        diffusion_part = d_ratio * (field[i+1] - 2 * field[i] + field[i-1])
        transport_part = -t_ratio * (field[i] - field[i-1])
        updated[i] = field[i] + diffusion_part + transport_part
    end
    updated[1] = 0.0
    updated[end] = 0.0
    return updated
end

grid_points = 61
diffusivity = 0.08
velocity = 0.4
dx = 1.0
dt = 0.2
steps = 120
d_ratio = diffusivity * dt / dx^2
t_ratio = velocity * dt / dx
field = initialize_field(grid_points)

println("step,time,center_value,total_mass,max_value,min_value,diffusion_ratio,transport_ratio,warning")
for step in 0:steps
    time = step * dt
    center_value = field[cld(grid_points, 2)]
    total_mass = sum(field) * dx
    println(join((step, time, center_value, total_mass, maximum(field), minimum(field), d_ratio, t_ratio, "Spatial dynamics depend on field meaning boundary conditions grid spacing time step and numerical stability."), ","))
    global field = update_advection_diffusion(field, d_ratio, t_ratio)
end
