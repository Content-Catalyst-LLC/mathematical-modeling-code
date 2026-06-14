.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then \
		c++ -O2 -std=c++17 continuity_break_diagnostics.cpp -o continuity_break_diagnostics; \
		mkdir -p ../outputs/tables; \
		./continuity_break_diagnostics > ../outputs/tables/cpp_continuity_break_diagnostics.csv; \
	else \
		echo "c++ compiler not found; skipping C++ workflow."; \
	fi

clean:
	rm -f continuity_break_diagnostics
