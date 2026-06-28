baseline = [
    10.0 2.0 0.0;
    1.0 12.0 3.0;
    0.0 4.0 8.0
]

intervention_effect = [
    1.0 0.5 0.0;
    0.2 1.5 0.4;
    0.0 0.7 1.2
]

stress_effect = [
    -0.5 -0.2 0.0;
    -0.1 -0.8 -0.3;
    0.0 -0.4 -0.9
]

combined_change = intervention_effect + 0.5 .* stress_effect
future = baseline + combined_change
difference = future - baseline
same_shape = size(baseline) == size(intervention_effect) == size(stress_effect)

println("operation_name,matrix_shape,compatible_shape,output_entry_sum,warning")
println(join((
    "baseline_plus_weighted_intervention_and_stress",
    string(size(baseline,1), "x", size(baseline,2)),
    same_shape,
    round(sum(difference), digits=4),
    "Shape compatibility is not enough; semantic compatibility must be documented."
), ","))
