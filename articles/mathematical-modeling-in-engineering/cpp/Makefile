.PHONY: run clean

run:
	c++ -O2 -std=c++17 engineering_design_summary.cpp -o engineering_design_summary
	./engineering_design_summary > ../outputs/tables/cpp_engineering_design_summary.csv 2> ../outputs/logs/cpp_engineering_design_stderr.log

clean:
	rm -f engineering_design_summary
