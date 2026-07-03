.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 orthogonal_approximation_audit.cpp -o orthogonal_approximation_audit_cpp && ./orthogonal_approximation_audit_cpp > ../outputs/tables/cpp_orthogonal_approximation_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f orthogonal_approximation_audit_cpp
