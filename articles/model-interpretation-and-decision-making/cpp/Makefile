.PHONY: run clean

run:
	c++ -O2 -std=c++17 decision_summary.cpp -o decision_summary
	./decision_summary > ../outputs/tables/cpp_decision_summary.csv 2> ../outputs/logs/cpp_decision_stderr.log

clean:
	rm -f decision_summary
