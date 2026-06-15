.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 change_of_variables_audit.cpp -o change_of_variables_audit; mkdir -p ../outputs/tables; ./change_of_variables_audit > ../outputs/tables/cpp_change_of_variables_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f change_of_variables_audit
