.PHONY: run clean

run:
	c++ -O2 -std=c++17 functional_forms.cpp -o functional_forms
	mkdir -p ../outputs/tables
	./functional_forms > ../outputs/tables/cpp_functional_forms.csv

clean:
	rm -f functional_forms
