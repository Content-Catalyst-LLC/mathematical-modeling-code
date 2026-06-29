.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 control_systems_audit.cpp -o control_systems_audit_cpp && ./control_systems_audit_cpp > ../outputs/tables/cpp_control_systems_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f control_systems_audit_cpp
