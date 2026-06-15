.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 nonlinear_dynamics_audit.cpp -o nonlinear_dynamics_audit; mkdir -p ../outputs/tables; ./nonlinear_dynamics_audit > ../outputs/tables/cpp_nonlinear_dynamics_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f nonlinear_dynamics_audit
