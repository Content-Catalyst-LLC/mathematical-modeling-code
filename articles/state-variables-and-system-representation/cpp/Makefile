.PHONY: run clean

run:
	c++ -O2 -std=c++17 state_representation_resource_model.cpp -o state_representation_resource_model
	./state_representation_resource_model > ../outputs/tables/cpp_state_representation_summary.txt

clean:
	rm -f state_representation_resource_model
