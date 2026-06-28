.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 rank_nullity_audit.cpp -o rank_nullity_audit_cpp && ./rank_nullity_audit_cpp > ../outputs/tables/cpp_rank_nullity_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f rank_nullity_audit_cpp
