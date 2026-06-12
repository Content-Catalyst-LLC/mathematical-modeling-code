.PHONY: run clean

run:
	c++ -O2 -std=c++17 probabilistic_risk_model.cpp -o probabilistic_risk_model
	./probabilistic_risk_model > ../outputs/tables/cpp_probabilistic_risk_summary.txt

clean:
	rm -f probabilistic_risk_model
