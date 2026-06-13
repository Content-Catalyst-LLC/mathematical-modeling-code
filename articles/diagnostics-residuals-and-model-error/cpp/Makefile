.PHONY: run clean

run:
	c++ -O2 -std=c++17 diagnostic_summary.cpp -o diagnostic_summary
	./diagnostic_summary > ../outputs/tables/cpp_diagnostic_summary.csv 2> ../outputs/logs/cpp_diagnostic_stderr.log

clean:
	rm -f diagnostic_summary
