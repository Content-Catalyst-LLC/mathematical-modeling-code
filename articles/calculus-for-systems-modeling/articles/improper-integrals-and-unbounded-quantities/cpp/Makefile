.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 improper_integral_audit.cpp -o improper_integral_audit; mkdir -p ../outputs/tables; ./improper_integral_audit > ../outputs/tables/cpp_improper_integral_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f improper_integral_audit
