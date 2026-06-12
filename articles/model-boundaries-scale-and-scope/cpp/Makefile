.PHONY: run clean

run:
	c++ -O2 -std=c++17 boundary_resource_model.cpp -o boundary_resource_model
	./boundary_resource_model > ../outputs/tables/cpp_boundary_resource_summary.txt

clean:
	rm -f boundary_resource_model
