.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 spatial_accumulation_audit.cpp -o spatial_accumulation_audit; mkdir -p ../outputs/tables; ./spatial_accumulation_audit > ../outputs/tables/cpp_spatial_accumulation_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f spatial_accumulation_audit
