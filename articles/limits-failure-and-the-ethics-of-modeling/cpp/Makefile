.PHONY: run clean

run:
	c++ -O2 -std=c++17 model_ethics_risk_summary.cpp -o model_ethics_risk_summary
	./model_ethics_risk_summary > ../outputs/tables/cpp_model_ethics_risk_summary.csv 2> ../outputs/logs/cpp_model_ethics_risk_stderr.log

clean:
	rm -f model_ethics_risk_summary
