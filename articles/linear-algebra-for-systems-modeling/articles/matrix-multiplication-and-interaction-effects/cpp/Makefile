.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 matrix_product_interaction_audit.cpp -o matrix_product_interaction_audit_cpp && ./matrix_product_interaction_audit_cpp > ../outputs/tables/cpp_matrix_product_interaction_audit.csv; else echo "c++ not found; skipping C++."; fi
clean:
	rm -f matrix_product_interaction_audit_cpp
