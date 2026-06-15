.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 trajectory_audit.cpp -o trajectory_audit; mkdir -p ../outputs/tables; ./trajectory_audit > ../outputs/tables/cpp_trajectory_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f trajectory_audit
