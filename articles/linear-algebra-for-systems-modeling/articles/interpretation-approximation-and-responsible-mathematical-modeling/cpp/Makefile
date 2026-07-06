.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 responsible_modeling_audit.cpp -o responsible_modeling_audit_cpp && ./responsible_modeling_audit_cpp > ../outputs/tables/cpp_responsible_modeling_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f responsible_modeling_audit_cpp
