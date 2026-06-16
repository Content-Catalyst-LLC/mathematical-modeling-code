co2_forcing(concentration, baseline=280.0) = 5.35 * log(concentration / baseline)

function one_box_temperature(forcing, feedback, heat_capacity, time; initial=0.0)
    equilibrium = forcing / feedback
    return equilibrium + (initial - equilibrium) * exp(-(feedback / heat_capacity) * time)
end

forcing = 3.7
heat_capacity = 8.0

println("time,weak_feedback,baseline_feedback,strong_feedback")
for t in 0:5:100
    weak = one_box_temperature(forcing, 0.9, heat_capacity, t)
    baseline = one_box_temperature(forcing, 1.2, heat_capacity, t)
    strong = one_box_temperature(forcing, 1.6, heat_capacity, t)
    println("$(t),$(weak),$(baseline),$(strong)")
end
