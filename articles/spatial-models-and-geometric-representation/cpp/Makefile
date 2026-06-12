.PHONY: run clean

run:
	c++ -O2 -std=c++17 spatial_distance_diagnostics.cpp -o spatial_distance_diagnostics
	./spatial_distance_diagnostics > ../outputs/tables/cpp_spatial_distance_diagnostics.csv

clean:
	rm -f spatial_distance_diagnostics
