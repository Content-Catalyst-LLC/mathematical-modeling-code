.PHONY: all smoke calculators python test r julia sql haskell c cpp fortran rust go advanced clean

all: python test r julia sql haskell c cpp fortran rust go advanced calculators

smoke: python sql advanced calculators

calculators:
	@if [ -f calculators/run_calculator_smoke_tests.sh ]; then cd calculators && bash run_calculator_smoke_tests.sh; else echo "calculator smoke tests not found."; fi

python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/approximation_error/cli.py --output-dir outputs; else echo "python3 not found; skipping Python workflow."; fi

test:
	@if command -v python3 >/dev/null 2>&1 && python3 -c "import pytest" >/dev/null 2>&1; then python3 -m pytest python/tests; else echo "pytest not found; skipping Python tests."; fi

r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/approximation_error_audit.R; else echo "Rscript not found; skipping R workflow."; fi

julia:
	@if command -v julia >/dev/null 2>&1; then julia julia/approximation_error_audit.jl > outputs/tables/julia_approximation_error_audit.csv; else echo "julia not found; skipping Julia workflow."; fi

sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/approximation_error.sqlite < sql/schema.sql; sqlite3 outputs/tables/approximation_error.sqlite < sql/analysis_queries.sql > outputs/tables/sql_approximation_error_report.txt; else echo "sqlite3 not found; skipping SQL workflow."; fi

haskell:
	$(MAKE) -C haskell run

c:
	@if command -v cc >/dev/null 2>&1; then cc -O2 -std=c11 c/approximation_error_audit.c -lm -o outputs/approximation_error_c; ./outputs/approximation_error_c > outputs/tables/c_approximation_error_audit.csv; else echo "cc not found; skipping C workflow."; fi

cpp:
	$(MAKE) -C cpp run

fortran:
	@if command -v gfortran >/dev/null 2>&1; then gfortran -O2 fortran/approximation_error_audit.f90 -o outputs/approximation_error_fortran; ./outputs/approximation_error_fortran > outputs/tables/fortran_approximation_error_audit.txt; else echo "gfortran not found; skipping Fortran workflow."; fi

rust:
	@if command -v cargo >/dev/null 2>&1; then cd rust && cargo run --quiet > ../outputs/tables/rust_approximation_error_audit.csv; else echo "cargo not found; skipping Rust workflow."; fi

go:
	@if command -v go >/dev/null 2>&1; then cd go && go run main.go > ../outputs/tables/go_approximation_error_audit.csv; else echo "go not found; skipping Go workflow."; fi

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log outputs/reports/*.md
	rm -f outputs/approximation_error_c outputs/approximation_error_fortran
	rm -f calculators/outputs/*.csv calculators/outputs/*.json calculators/outputs/*.txt
	$(MAKE) -C haskell clean || true
	$(MAKE) -C cpp clean || true
	$(MAKE) -C advanced clean || true
	cd rust && cargo clean || true
