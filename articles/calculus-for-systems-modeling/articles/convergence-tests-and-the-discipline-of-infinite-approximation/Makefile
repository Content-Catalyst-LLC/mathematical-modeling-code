.PHONY: all smoke calculators python r sql advanced clean

all: python r sql advanced calculators

smoke: python sql advanced calculators

calculators:
	@if [ -f calculators/run_calculator_smoke_tests.sh ]; then cd calculators && bash run_calculator_smoke_tests.sh; else echo "calculator smoke tests not found."; fi

python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/convergence_tests/cli.py --output-dir outputs; else echo "python3 not found; skipping Python workflow."; fi

r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/convergence_test_audit.R; else echo "Rscript not found; skipping R workflow."; fi

sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/convergence_tests.sqlite < sql/schema.sql; sqlite3 outputs/tables/convergence_tests.sqlite < sql/analysis_queries.sql > outputs/tables/sql_convergence_test_report.txt; else echo "sqlite3 not found; skipping SQL workflow."; fi

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log outputs/reports/*.md
	rm -f calculators/outputs/*.csv calculators/outputs/*.json calculators/outputs/*.txt
	$(MAKE) -C advanced clean || true
