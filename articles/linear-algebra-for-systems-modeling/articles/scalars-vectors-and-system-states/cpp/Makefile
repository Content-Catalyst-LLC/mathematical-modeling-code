.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 state_vector_audit.cpp -o state_vector_audit_cpp && ./state_vector_audit_cpp > ../outputs/tables/cpp_state_vector_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f state_vector_audit_cpp
