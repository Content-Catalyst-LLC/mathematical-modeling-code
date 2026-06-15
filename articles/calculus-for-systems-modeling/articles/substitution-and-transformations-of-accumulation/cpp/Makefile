.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 substitution_audit.cpp -o substitution_audit; mkdir -p ../outputs/tables; ./substitution_audit > ../outputs/tables/cpp_substitution_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f substitution_audit
