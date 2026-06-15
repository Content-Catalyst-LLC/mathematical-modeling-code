.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 taylor_audit.cpp -o taylor_audit; mkdir -p ../outputs/tables; ./taylor_audit > ../outputs/tables/cpp_taylor_approximation_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f taylor_audit
