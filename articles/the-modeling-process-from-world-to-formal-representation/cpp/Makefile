.PHONY: run clean

run:
	c++ -O2 -std=c++17 reservoir_model.cpp -o reservoir_model
	./reservoir_model > ../outputs/tables/cpp_reservoir_summary.txt

clean:
	rm -f reservoir_model
