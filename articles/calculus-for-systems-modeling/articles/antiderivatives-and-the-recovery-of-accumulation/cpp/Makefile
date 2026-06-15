.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 antiderivative_recovery_audit.cpp -o antiderivative_recovery_audit; mkdir -p ../outputs/tables; ./antiderivative_recovery_audit > ../outputs/tables/cpp_antiderivative_recovery_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f antiderivative_recovery_audit
