grid_points=61; diffusivity=0.08; dx=1.0; dt=0.2; steps=120
ratio=diffusivity*dt/dx^2
status=ratio<=0.5 ? "stable_for_basic_explicit_1d_diffusion" : "unstable_risk"
field=zeros(Float64, grid_points); field[cld(grid_points,2)]=1.0
println("step,time,center_value,total_mass,max_value,left_boundary,right_boundary,diffusion_ratio,stability_status")
for step in 0:steps
    println(join((step, step*dt, field[cld(grid_points,2)], sum(field)*dx, maximum(field), field[1], field[end], ratio, status), ","))
    updated=copy(field)
    for i in 2:(grid_points-1)
        updated[i]=field[i]+ratio*(field[i+1]-2*field[i]+field[i-1])
    end
    updated[1]=0.0; updated[end]=0.0
    global field=updated
end
