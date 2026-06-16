.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 stability_error_convergence.cpp -o stability_error_convergence; mkdir -p ../outputs/tables; ./stability_error_convergence > ../outputs/tables/cpp_convergence_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f stability_error_convergence
