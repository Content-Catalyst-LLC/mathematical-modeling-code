.PHONY: run clean

run:
	c++ -O2 -std=c++17 logistic_model.cpp -o logistic_model
	./logistic_model > ../outputs/tables/cpp_logistic_summary.txt

clean:
	rm -f logistic_model
