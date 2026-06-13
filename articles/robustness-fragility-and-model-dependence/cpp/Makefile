.PHONY: run clean

run:
	c++ -O2 -std=c++17 robustness_summary.cpp -o robustness_summary
	./robustness_summary > ../outputs/tables/cpp_robustness_summary.csv 2> ../outputs/logs/cpp_robustness_stderr.log

clean:
	rm -f robustness_summary
