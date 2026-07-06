.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 machine_learning_linear_structure_audit.cpp -o machine_learning_linear_structure_audit_cpp && ./machine_learning_linear_structure_audit_cpp > ../outputs/tables/cpp_machine_learning_linear_structure_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f machine_learning_linear_structure_audit_cpp
