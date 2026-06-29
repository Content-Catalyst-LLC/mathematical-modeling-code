result <- data.frame(calculator="matrix_product_calculator", left_shape="2x3", right_shape="3x2", product_shape="2x2", product_matrix="1.040000,0.560000;0.585000,0.940000", reverse_product_available=TRUE, warning="Matrix products require order, intermediate-layer meaning, units, row-column alignment, and pathway validity review.")
dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_matrix_product_calculator.csv", row.names = FALSE)
print(result)
