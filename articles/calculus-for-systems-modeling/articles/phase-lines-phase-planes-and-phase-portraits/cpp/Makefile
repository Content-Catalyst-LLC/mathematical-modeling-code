.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 phase_portrait_audit.cpp -o phase_portrait_audit; mkdir -p ../outputs/tables; ./phase_portrait_audit > ../outputs/tables/cpp_phase_portrait_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f phase_portrait_audit
