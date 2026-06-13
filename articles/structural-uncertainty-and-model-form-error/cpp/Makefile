.PHONY: run clean

run:
	c++ -O2 -std=c++17 structural_summary.cpp -o structural_summary
	./structural_summary > ../outputs/tables/cpp_structural_summary.csv 2> ../outputs/logs/cpp_structural_stderr.log

clean:
	rm -f structural_summary
