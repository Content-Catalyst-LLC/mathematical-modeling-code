.PHONY: smoke report test clean

smoke: report test

report:
	python3 python/generate_advanced_report.py

test:
	@if python3 -c "import pytest" >/dev/null 2>&1; then \
		python3 -m pytest python/test_advanced_differentiability.py; \
	else \
		echo "pytest not found; running built-in assertions instead."; \
		python3 python/test_advanced_differentiability.py; \
	fi

clean:
	rm -f outputs/reports/*.md outputs/json/*.json outputs/tables/*.csv
