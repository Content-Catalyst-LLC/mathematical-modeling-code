.PHONY: run clean

run:
	c++ -O2 -std=c++17 abm_adoption_model.cpp -o abm_adoption_model
	./abm_adoption_model > ../outputs/tables/cpp_abm_adoption_trajectory.csv

clean:
	rm -f abm_adoption_model
