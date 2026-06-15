function initialize_field(grid_points)
    field = zeros(Float64, grid_points)
    field[cld(grid_points, 2)] = 1.0
    return field
end

function diffusion_step(field, ratio)
    updated = copy(field)
    for i in 2:(length(field)-1)
        updated[i] = field[i] + ratio * (field[i+1] - 2 * field[i] + field[i-1])
    end
    updated[1] = 0.0
    updated[end] = 0.0
    return updated
end

grid_points = 51
diffusivity = 0.1
dx = 1.0
dt = 0.25
steps = 100
ratio = diffusivity * dt / dx^2
field = initialize_field(grid_points)

println("step,time,center_value,total_mass,max_value,min_value,stability_ratio,warning")
for step in 0:steps
    time = step * dt
    center_value = field[cld(grid_points, 2)]
    total_mass = sum(field) * dx
    println(join((step, time, center_value, total_mass, maximum(field), minimum(field), ratio, "Explicit diffusion schemes require stability checks boundary and grid assumptions shape results."), ","))
    global field = diffusion_step(field, ratio)
end
