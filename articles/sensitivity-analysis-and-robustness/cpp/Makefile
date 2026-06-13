.PHONY: run clean

run:
	c++ -O2 -std=c++17 sensitivity_summary.cpp -o sensitivity_summary
	./sensitivity_summary > ../outputs/tables/cpp_sensitivity_summary.csv 2> ../outputs/logs/cpp_sensitivity_stderr.log

clean:
	rm -f sensitivity_summary
