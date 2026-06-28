.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 least_squares_audit.cpp -o least_squares_audit_cpp && ./least_squares_audit_cpp > ../outputs/tables/cpp_least_squares_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f least_squares_audit_cpp
