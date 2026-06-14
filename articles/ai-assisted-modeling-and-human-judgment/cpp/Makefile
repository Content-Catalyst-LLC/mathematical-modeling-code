.PHONY: run clean

run:
	c++ -O2 -std=c++17 human_judgment_risk_summary.cpp -o human_judgment_risk_summary
	./human_judgment_risk_summary > ../outputs/tables/cpp_human_judgment_risk_summary.csv 2> ../outputs/logs/cpp_human_judgment_risk_stderr.log

clean:
	rm -f human_judgment_risk_summary
