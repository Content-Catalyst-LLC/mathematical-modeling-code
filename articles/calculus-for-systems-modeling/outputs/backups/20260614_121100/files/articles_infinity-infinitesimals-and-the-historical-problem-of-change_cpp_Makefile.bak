.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then \
		c++ -O2 -std=c++17 difference_quotient.cpp -o difference_quotient; \
		mkdir -p ../outputs/tables; \
		./difference_quotient > ../outputs/tables/cpp_difference_quotient.csv; \
	else \
		echo "c++ compiler not found; skipping C++ workflow."; \
	fi

clean:
	rm -f difference_quotient
