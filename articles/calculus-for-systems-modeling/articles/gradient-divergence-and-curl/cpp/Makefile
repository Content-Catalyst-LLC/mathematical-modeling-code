.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 field_operator_audit.cpp -o field_operator_audit; mkdir -p ../outputs/tables; ./field_operator_audit > ../outputs/tables/cpp_field_operator_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f field_operator_audit
