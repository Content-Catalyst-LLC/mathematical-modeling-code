.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 jacobian_audit.cpp -o jacobian_audit; mkdir -p ../outputs/tables; ./jacobian_audit > ../outputs/tables/cpp_jacobian_transformation_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f jacobian_audit
