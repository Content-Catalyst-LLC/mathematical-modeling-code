.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 stiff_systems_difficulty.cpp -o stiff_systems_difficulty; mkdir -p ../outputs/tables; ./stiff_systems_difficulty > ../outputs/tables/cpp_stiffness_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f stiff_systems_difficulty
