.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 pagerank_network_influence_audit.cpp -o pagerank_network_influence_audit_cpp && ./pagerank_network_influence_audit_cpp > ../outputs/tables/cpp_pagerank_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f pagerank_network_influence_audit_cpp
