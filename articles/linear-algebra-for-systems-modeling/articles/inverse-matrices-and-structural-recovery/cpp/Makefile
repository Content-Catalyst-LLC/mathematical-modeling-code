.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 inverse_recovery_audit.cpp -o inverse_recovery_audit_cpp && ./inverse_recovery_audit_cpp > ../outputs/tables/cpp_inverse_recovery_audit.csv; else echo "c++ not found; skipping C++."; fi
clean:
	rm -f inverse_recovery_audit_cpp
