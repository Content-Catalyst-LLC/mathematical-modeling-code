.PHONY: run clean
run:
	c++ -O2 -std=c++17 future_modeling_priority_summary.cpp -o future_modeling_priority_summary
	./future_modeling_priority_summary > ../outputs/tables/cpp_future_modeling_priority_summary.csv 2> ../outputs/logs/cpp_future_modeling_priority_stderr.log
clean:
	rm -f future_modeling_priority_summary
