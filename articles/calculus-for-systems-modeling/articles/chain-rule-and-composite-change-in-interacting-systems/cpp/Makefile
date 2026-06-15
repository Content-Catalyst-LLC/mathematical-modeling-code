.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 chain_rule_pathway_audit.cpp -o chain_rule_pathway_audit; mkdir -p ../outputs/tables; ./chain_rule_pathway_audit > ../outputs/tables/cpp_chain_rule_pathway_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f chain_rule_pathway_audit
