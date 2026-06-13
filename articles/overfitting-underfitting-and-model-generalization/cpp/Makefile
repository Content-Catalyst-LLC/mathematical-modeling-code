.PHONY: run clean

run:
	c++ -O2 -std=c++17 generalization_summary.cpp -o generalization_summary
	./generalization_summary > ../outputs/tables/cpp_generalization_summary.csv 2> ../outputs/logs/cpp_generalization_stderr.log

clean:
	rm -f generalization_summary
