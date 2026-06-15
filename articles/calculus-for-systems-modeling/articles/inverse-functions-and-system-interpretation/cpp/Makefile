.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 inverse_interpretation_audit.cpp -o inverse_interpretation_audit; mkdir -p ../outputs/tables; ./inverse_interpretation_audit > ../outputs/tables/cpp_inverse_interpretation_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f inverse_interpretation_audit
