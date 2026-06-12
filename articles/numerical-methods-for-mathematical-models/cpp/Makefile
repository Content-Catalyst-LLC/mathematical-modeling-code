.PHONY: run clean

run:
	c++ -O2 -std=c++17 euler_resource_model.cpp -o euler_resource_model
	./euler_resource_model > ../outputs/tables/cpp_euler_convergence_summary.csv

clean:
	rm -f euler_resource_model
