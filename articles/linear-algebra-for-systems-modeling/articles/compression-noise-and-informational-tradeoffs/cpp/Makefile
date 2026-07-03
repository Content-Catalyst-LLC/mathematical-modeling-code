.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 compression_noise_audit.cpp -o compression_noise_audit_cpp && ./compression_noise_audit_cpp > ../outputs/tables/cpp_compression_noise_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f compression_noise_audit_cpp
