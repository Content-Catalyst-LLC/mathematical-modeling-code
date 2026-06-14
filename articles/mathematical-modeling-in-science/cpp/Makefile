.PHONY: run clean

run:
	c++ -O2 -std=c++17 population_science_summary.cpp -o population_science_summary
	./population_science_summary > ../outputs/tables/cpp_population_science_summary.csv 2> ../outputs/logs/cpp_population_science_stderr.log

clean:
	rm -f population_science_summary
