.PHONY: run clean

run:
	c++ -O2 -std=c++17 validation_error_summary.cpp -o validation_error_summary
	./validation_error_summary > ../outputs/tables/cpp_validation_summary.csv

clean:
	rm -f validation_error_summary
