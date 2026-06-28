result <- data.frame(
  calculator = "linear_transformation_calculator",
  row_count = 3,
  column_count = 3,
  input_state = "100.000000,60.000000,30.000000",
  output_state = "126.000000,75.500000,42.000000",
  rank = 3,
  nullity = 0,
  input_norm = 120.415946,
  output_norm = 152.750205,
  amplification_ratio = 1.268531,
  warning = "Matrix action shows modeled behavior; row meanings, column meanings, units, scaling, and sensitivity still require review."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_linear_transformation_calculator.csv", row.names = FALSE)
print(result)
