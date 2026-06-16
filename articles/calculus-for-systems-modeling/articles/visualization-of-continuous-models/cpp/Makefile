.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 continuous_model_visualization.cpp -o continuous_model_visualization; mkdir -p ../outputs/tables; ./continuous_model_visualization > ../outputs/tables/cpp_visualization_audit_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f continuous_model_visualization
