.PHONY: run clean

run:
	c++ -O2 -std=c++17 model_purpose_resource_model.cpp -o model_purpose_resource_model
	./model_purpose_resource_model > ../outputs/tables/cpp_model_purpose_resource_summary.txt

clean:
	rm -f model_purpose_resource_model
