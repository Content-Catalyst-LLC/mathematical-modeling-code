.PHONY: run clean

run:
	c++ -O2 -std=c++17 governance_risk_summary.cpp -o governance_risk_summary
	./governance_risk_summary > ../outputs/tables/cpp_governance_risk_summary.csv 2> ../outputs/logs/cpp_governance_risk_stderr.log

clean:
	rm -f governance_risk_summary
