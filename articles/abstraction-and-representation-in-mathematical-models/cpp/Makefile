.PHONY: run clean

run:
	c++ -O2 -std=c++17 stock_flow_model.cpp -o stock_flow_model
	./stock_flow_model > ../outputs/tables/cpp_stock_flow_summary.txt

clean:
	rm -f stock_flow_model
