.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 decomposition_workflow_audit.cpp -o decomposition_workflow_audit_cpp && ./decomposition_workflow_audit_cpp > ../outputs/tables/cpp_decomposition_workflow_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f decomposition_workflow_audit_cpp
