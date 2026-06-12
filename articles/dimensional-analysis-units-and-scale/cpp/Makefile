.PHONY: run clean

run:
	c++ -O2 -std=c++17 unit_scale_resource_model.cpp -o unit_scale_resource_model
	./unit_scale_resource_model > ../outputs/tables/cpp_unit_scale_summary.txt

clean:
	rm -f unit_scale_resource_model
