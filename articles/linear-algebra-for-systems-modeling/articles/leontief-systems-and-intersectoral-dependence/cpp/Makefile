.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 leontief_system_audit.cpp -o leontief_system_audit_cpp && ./leontief_system_audit_cpp > ../outputs/tables/cpp_leontief_system_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f leontief_system_audit_cpp
