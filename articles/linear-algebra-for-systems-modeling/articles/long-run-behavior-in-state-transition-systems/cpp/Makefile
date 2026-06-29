.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 long_run_transition_audit.cpp -o long_run_transition_audit_cpp && ./long_run_transition_audit_cpp > ../outputs/tables/cpp_long_run_transition_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f long_run_transition_audit_cpp
