.PHONY: smoke report test clean

smoke: report test

report:
	python3 python/generate_advanced_report.py

test:
	@if python3 -c "import pytest" >/dev/null 2>&1; then python3 -m pytest python/test_advanced_elasticity_sensitivity.py; else python3 python/test_advanced_elasticity_sensitivity.py; fi

clean:
	rm -f outputs/reports/*.md outputs/json/*.json outputs/tables/*.csv
