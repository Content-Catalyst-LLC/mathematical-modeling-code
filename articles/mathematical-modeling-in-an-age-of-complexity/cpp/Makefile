.PHONY: run clean

run:
	c++ -O2 -std=c++17 complexity_scenario_summary.cpp -o complexity_scenario_summary
	./complexity_scenario_summary > ../outputs/tables/cpp_complexity_scenario_summary.csv 2> ../outputs/logs/cpp_complexity_scenario_stderr.log

clean:
	rm -f complexity_scenario_summary
