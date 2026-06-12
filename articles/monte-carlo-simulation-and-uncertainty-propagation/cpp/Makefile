.PHONY: run clean

run:
	c++ -O2 -std=c++17 monte_carlo_resource_model.cpp -o monte_carlo_resource_model
	./monte_carlo_resource_model > ../outputs/tables/cpp_monte_carlo_resource_summary.csv

clean:
	rm -f monte_carlo_resource_model
