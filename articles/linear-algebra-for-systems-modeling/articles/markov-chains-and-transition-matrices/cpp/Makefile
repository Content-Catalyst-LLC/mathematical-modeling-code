.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 markov_transition_audit.cpp -o markov_transition_audit_cpp && ./markov_transition_audit_cpp > ../outputs/tables/cpp_markov_transition_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f markov_transition_audit_cpp
