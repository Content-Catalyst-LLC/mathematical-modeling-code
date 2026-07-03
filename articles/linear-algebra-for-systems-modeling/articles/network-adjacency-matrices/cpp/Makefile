.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 network_adjacency_audit.cpp -o network_adjacency_audit_cpp && ./network_adjacency_audit_cpp > ../outputs/tables/cpp_network_adjacency_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f network_adjacency_audit_cpp
