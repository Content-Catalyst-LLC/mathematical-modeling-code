.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 orthogonality_audit.cpp -o orthogonality_audit_cpp && ./orthogonality_audit_cpp > ../outputs/tables/cpp_orthogonality_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f orthogonality_audit_cpp
