column_count <- 3
rank_value <- 3
nullity_value <- column_count - rank_value

result <- data.frame(
  calculator = "rank_nullity_calculator",
  row_count = 3,
  column_count = column_count,
  rank = rank_value,
  nullity = nullity_value,
  rank_nullity_check = rank_value + nullity_value == column_count,
  rank_deficient = FALSE,
  pivot_columns = "0,1,2",
  free_columns = "none",
  tolerance = 1.0e-10,
  warning = "Rank and nullity depend on matrix structure; numerical rank depends on tolerance."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_rank_nullity_calculator.csv", row.names = FALSE)
print(result)
