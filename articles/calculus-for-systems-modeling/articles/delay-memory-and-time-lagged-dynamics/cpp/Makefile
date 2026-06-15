.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 delay_memory_audit.cpp -o delay_memory_audit; mkdir -p ../outputs/tables; ./delay_memory_audit > ../outputs/tables/cpp_delay_memory_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f delay_memory_audit
