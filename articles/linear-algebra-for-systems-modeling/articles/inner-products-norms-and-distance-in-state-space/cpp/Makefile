.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 state_space_geometry_audit.cpp -o state_space_geometry_audit_cpp && ./state_space_geometry_audit_cpp > ../outputs/tables/cpp_state_space_geometry_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f state_space_geometry_audit_cpp
