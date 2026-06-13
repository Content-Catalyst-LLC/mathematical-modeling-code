.PHONY: run clean

run:
	c++ -O2 -std=c++17 uncertainty_summary.cpp -o uncertainty_summary
	./uncertainty_summary > ../outputs/tables/cpp_uncertainty_summary.csv 2> ../outputs/logs/cpp_uncertainty_stderr.log

clean:
	rm -f uncertainty_summary
