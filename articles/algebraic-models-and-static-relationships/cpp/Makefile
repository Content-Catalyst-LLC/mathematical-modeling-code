.PHONY: run clean

run:
	c++ -O2 -std=c++17 static_allocation_model.cpp -o static_allocation_model
	./static_allocation_model > ../outputs/tables/cpp_static_allocation_summary.txt

clean:
	rm -f static_allocation_model
