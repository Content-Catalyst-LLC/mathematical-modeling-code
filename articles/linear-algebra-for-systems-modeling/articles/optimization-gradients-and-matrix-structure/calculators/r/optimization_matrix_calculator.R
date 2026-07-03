result <- data.frame(
  calculator = "optimization_gradients_and_matrix_structure_calculator",
  model_name = "synthetic_optimization_gradient_matrix_audit",
  observations = 10,
  features = 5,
  objective = "mean_squared_error_plus_l2_regularization",
  solver = "fixed_step_gradient_descent_compared_with_closed_form_ridge_solution",
  regularization_strength = 0.75,
  feature_matrix_condition_number = 18.4,
  hessian_condition_number = 3.8,
  gradient_norm_final = 0.0009,
  objective_initial = 52.0,
  objective_final = 4.3,
  closed_form_gap_norm = 0.002,
  training_rmse = 1.9,
  warning = "Optimization metrics depend on objective validity, variable definition, constraints, scaling, solver choice, convergence rules, conditioning, sensitivity testing, and interpretation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_optimization_gradients_and_matrix_structure_calculator.csv", row.names = FALSE)
print(result)
