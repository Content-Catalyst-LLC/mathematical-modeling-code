.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 input_output_audit.cpp -o input_output_audit_cpp && ./input_output_audit_cpp > ../outputs/tables/cpp_input_output_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f input_output_audit_cpp
