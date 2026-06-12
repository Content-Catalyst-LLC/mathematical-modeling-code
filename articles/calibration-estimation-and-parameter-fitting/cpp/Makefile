.PHONY: run clean

run:
	c++ -O2 -std=c++17 calibration_resource_fit.cpp -o calibration_resource_fit
	./calibration_resource_fit > ../outputs/tables/cpp_calibration_summary.csv

clean:
	rm -f calibration_resource_fit
