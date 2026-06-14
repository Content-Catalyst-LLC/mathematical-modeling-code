.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then \
		c++ -O2 -std=c++17 differentiability_diagnostics.cpp -o differentiability_diagnostics; \
		mkdir -p ../outputs/tables; \
		./differentiability_diagnostics > ../outputs/tables/cpp_differentiability_diagnostics.csv; \
	else \
		echo "c++ compiler not found; skipping C++ workflow."; \
	fi

clean:
	rm -f differentiability_diagnostics
