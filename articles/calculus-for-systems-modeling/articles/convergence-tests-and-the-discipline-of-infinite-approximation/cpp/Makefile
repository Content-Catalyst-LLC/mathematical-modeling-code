.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 convergence_test_audit.cpp -o convergence_test_audit; mkdir -p ../outputs/tables; ./convergence_test_audit > ../outputs/tables/cpp_convergence_test_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f convergence_test_audit
