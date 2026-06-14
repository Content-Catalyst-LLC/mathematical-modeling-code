.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then \
		c++ -O2 -std=c++17 limit_convergence.cpp -o limit_convergence; \
		mkdir -p ../outputs/tables; \
		./limit_convergence > ../outputs/tables/cpp_limit_convergence.csv; \
	else \
		echo "c++ compiler not found; skipping C++ workflow."; \
	fi

clean:
	rm -f limit_convergence
