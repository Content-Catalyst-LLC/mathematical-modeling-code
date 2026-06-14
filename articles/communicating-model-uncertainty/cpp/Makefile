.PHONY: run clean

run:
	c++ -O2 -std=c++17 communication_summary.cpp -o communication_summary
	./communication_summary > ../outputs/tables/cpp_communication_summary.csv 2> ../outputs/logs/cpp_communication_stderr.log

clean:
	rm -f communication_summary
