.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 surface_integral_audit.cpp -o surface_integral_audit; mkdir -p ../outputs/tables; ./surface_integral_audit > ../outputs/tables/cpp_surface_integral_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f surface_integral_audit
