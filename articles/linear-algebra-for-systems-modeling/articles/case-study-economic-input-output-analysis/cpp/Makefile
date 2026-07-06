.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 economic_input_output_audit.cpp -o economic_input_output_audit_cpp && ./economic_input_output_audit_cpp > ../outputs/tables/cpp_economic_input_output_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f economic_input_output_audit_cpp
