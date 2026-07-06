.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 state_transition_markov_audit.cpp -o state_transition_markov_audit_cpp && ./state_transition_markov_audit_cpp > ../outputs/tables/cpp_state_transition_markov_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f state_transition_markov_audit_cpp
