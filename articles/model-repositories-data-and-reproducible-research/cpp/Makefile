.PHONY: run clean

run:
	c++ -O2 -std=c++17 repository_inventory_summary.cpp -o repository_inventory_summary
	./repository_inventory_summary > ../outputs/tables/cpp_repository_inventory_summary.csv

clean:
	rm -f repository_inventory_summary
