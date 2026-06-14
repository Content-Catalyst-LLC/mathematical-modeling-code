.PHONY: run clean

run:
	c++ -O2 -std=c++17 sustainability_scenario_summary.cpp -o sustainability_scenario_summary
	./sustainability_scenario_summary > ../outputs/tables/cpp_sustainability_scenario_summary.csv 2> ../outputs/logs/cpp_sustainability_scenario_stderr.log

clean:
	rm -f sustainability_scenario_summary
