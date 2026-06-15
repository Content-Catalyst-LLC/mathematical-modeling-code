.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 equilibrium_stability_audit.cpp -o equilibrium_stability_audit; mkdir -p ../outputs/tables; ./equilibrium_stability_audit > ../outputs/tables/cpp_equilibrium_stability_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f equilibrium_stability_audit
