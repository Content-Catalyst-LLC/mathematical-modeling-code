.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 hessian_audit.cpp -o hessian_audit; mkdir -p ../outputs/tables; ./hessian_audit > ../outputs/tables/cpp_hessian_curvature_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f hessian_audit
