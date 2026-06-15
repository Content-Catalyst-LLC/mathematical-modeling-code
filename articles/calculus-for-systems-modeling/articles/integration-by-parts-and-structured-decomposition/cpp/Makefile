.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 integration_by_parts_audit.cpp -o integration_by_parts_audit; mkdir -p ../outputs/tables; ./integration_by_parts_audit > ../outputs/tables/cpp_integration_by_parts_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f integration_by_parts_audit
