.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 linearity_distortion_audit.cpp -o linearity_distortion_audit_cpp && ./linearity_distortion_audit_cpp > ../outputs/tables/cpp_linearity_distortion_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f linearity_distortion_audit_cpp
