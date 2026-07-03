.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 graph_theory_foundations_audit.cpp -o graph_theory_foundations_audit_cpp && ./graph_theory_foundations_audit_cpp > ../outputs/tables/cpp_graph_theory_foundations_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f graph_theory_foundations_audit_cpp
