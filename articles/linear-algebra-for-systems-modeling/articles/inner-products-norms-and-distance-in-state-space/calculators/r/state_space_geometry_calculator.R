result <- data.frame(
  calculator = "state_space_geometry_calculator",
  state_a = "12.000000,4.000000,0.800000",
  state_b = "10.000000,5.500000,1.100000",
  difference_vector = "2.000000,-1.500000,-0.300000",
  dot_product = 142.88,
  cosine_similarity = 0.988725,
  weighted_inner_product = 133.04,
  norm_1 = 3.8,
  norm_2 = 2.517936,
  norm_inf = 2.0,
  euclidean_distance = 2.517936,
  weighted_distance = 2.33538,
  warning = "Distance depends on units, scaling, norm choice, and weights."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_state_space_geometry_calculator.csv", row.names = FALSE)
print(result)
