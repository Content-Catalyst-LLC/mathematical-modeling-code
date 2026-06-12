.PHONY: run clean

run:
	c++ -O2 -std=c++17 model_selection_summary.cpp -o model_selection_summary
	./model_selection_summary > ../outputs/tables/cpp_model_selection_summary.csv 2> ../outputs/logs/cpp_model_selection_stderr.log

clean:
	rm -f model_selection_summary
