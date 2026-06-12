.PHONY: run clean

run:
	c++ -O2 -std=c++17 workflow_resource_model.cpp -o workflow_resource_model
	./workflow_resource_model > ../outputs/tables/cpp_workflow_resource_model.csv

clean:
	rm -f workflow_resource_model
