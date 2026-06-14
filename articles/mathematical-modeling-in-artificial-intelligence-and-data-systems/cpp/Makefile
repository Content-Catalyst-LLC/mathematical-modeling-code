.PHONY: run clean

run:
	c++ -O2 -std=c++17 ai_candidate_governance_summary.cpp -o ai_candidate_governance_summary
	./ai_candidate_governance_summary > ../outputs/tables/cpp_ai_candidate_governance_summary.csv 2> ../outputs/logs/cpp_ai_candidate_governance_stderr.log

clean:
	rm -f ai_candidate_governance_summary
