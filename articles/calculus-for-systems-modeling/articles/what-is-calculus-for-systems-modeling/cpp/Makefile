.PHONY: run clean

run:
	c++ -O2 -std=c++17 dynamic_model.cpp -o dynamic_model
	mkdir -p ../outputs/tables
	./dynamic_model > ../outputs/tables/cpp_dynamic_model.csv

clean:
	rm -f dynamic_model
