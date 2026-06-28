row_count = 4
column_count = 2
rank_value = 2
overdetermined = row_count > column_count
solution = "0.850000;1.040000"
fitted_values = "1.890000;2.930000;3.970000;5.010000"
residuals = "0.110000;-0.030000;0.130000;0.090000"
residual_norm = 0.191311

println("system_name,row_count,column_count,overdetermined,rank,solution,fitted_values,residuals,residual_norm,solver_method,warning")
println(join((
    "four_observation_linear_calibration",
    row_count,
    column_count,
    overdetermined,
    rank_value,
    solution,
    fitted_values,
    residuals,
    residual_norm,
    "least squares audit record",
    "Least squares fit requires residual rank conditioning and model-purpose review."
), ","))
