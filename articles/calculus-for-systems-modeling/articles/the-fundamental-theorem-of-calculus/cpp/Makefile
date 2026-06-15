.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 fundamental_theorem_audit.cpp -o fundamental_theorem_audit; mkdir -p ../outputs/tables; ./fundamental_theorem_audit > ../outputs/tables/cpp_fundamental_theorem_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f fundamental_theorem_audit
