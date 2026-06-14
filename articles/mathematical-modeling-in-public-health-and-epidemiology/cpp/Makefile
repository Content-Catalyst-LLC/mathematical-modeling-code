.PHONY: run clean

run:
	c++ -O2 -std=c++17 epidemic_scenario_summary.cpp -o epidemic_scenario_summary
	./epidemic_scenario_summary > ../outputs/tables/cpp_epidemic_scenario_summary.csv 2> ../outputs/logs/cpp_epidemic_scenario_stderr.log

clean:
	rm -f epidemic_scenario_summary
