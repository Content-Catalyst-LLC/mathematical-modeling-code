duration = [1.0,1.0,1.0,1.0,1.0]
inflow = [12.0,10.0,9.0,8.0,7.0]
outflow = [6.0,7.0,8.0,9.0,9.0]
exposure_intensity = [20.0,18.0,15.0,13.0,11.0]
population_weight = [1000.0,1100.0,1050.0,980.0,960.0]
initial_stock = 50.0

cumulative_inflow = sum(inflow .* duration)
cumulative_outflow = sum(outflow .* duration)
net_accumulation = cumulative_inflow - cumulative_outflow
ending_stock = initial_stock + net_accumulation
cumulative_exposure = sum(exposure_intensity .* duration)
population_weighted_exposure = sum(exposure_intensity .* population_weight .* duration)
gross_activity = cumulative_inflow + cumulative_outflow

println("initial_stock,cumulative_inflow,cumulative_outflow,net_accumulation,ending_stock,cumulative_exposure,population_weighted_exposure,gross_activity,method")
println("$initial_stock,$cumulative_inflow,$cumulative_outflow,$net_accumulation,$ending_stock,$cumulative_exposure,$population_weighted_exposure,$gross_activity,discrete time-step accumulation")
