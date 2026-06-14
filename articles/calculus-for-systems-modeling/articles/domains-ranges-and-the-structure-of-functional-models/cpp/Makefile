.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 domain_range_validation.cpp -o domain_range_validation; mkdir -p ../outputs/tables; ./domain_range_validation > ../outputs/tables/cpp_domain_range_validation.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f domain_range_validation
