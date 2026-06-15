.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 quotient_rule_audit.cpp -o quotient_rule_audit; mkdir -p ../outputs/tables; ./quotient_rule_audit > ../outputs/tables/cpp_quotient_rule_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f quotient_rule_audit
