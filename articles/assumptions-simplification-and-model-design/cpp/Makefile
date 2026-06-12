.PHONY: run clean

run:
	c++ -O2 -std=c++17 resource_model.cpp -o resource_model
	./resource_model > ../outputs/tables/cpp_resource_summary.txt

clean:
	rm -f resource_model
