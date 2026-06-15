.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 flux_circulation_audit.cpp -o flux_circulation_audit; mkdir -p ../outputs/tables; ./flux_circulation_audit > ../outputs/tables/cpp_flux_circulation_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f flux_circulation_audit
