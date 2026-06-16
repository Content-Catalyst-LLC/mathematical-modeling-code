.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 runge_kutta_audit.cpp -o runge_kutta_audit; mkdir -p ../outputs/tables; ./runge_kutta_audit > ../outputs/tables/cpp_runge_kutta_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f runge_kutta_audit
