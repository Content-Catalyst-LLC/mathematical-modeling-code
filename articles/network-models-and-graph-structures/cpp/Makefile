.PHONY: run clean

run:
	c++ -O2 -std=c++17 network_graph_diagnostics.cpp -o network_graph_diagnostics
	./network_graph_diagnostics > ../outputs/tables/cpp_network_graph_diagnostics.txt

clean:
	rm -f network_graph_diagnostics
