.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 latent_structure_audit.cpp -o latent_structure_audit_cpp && ./latent_structure_audit_cpp > ../outputs/tables/cpp_latent_structure_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f latent_structure_audit_cpp
