.PHONY: all smoke calculators python r julia sql haskell c cpp fortran rust go advanced clean

all: python r julia sql haskell c cpp fortran rust go advanced calculators

smoke: python sql advanced calculators

calculators:
	@if [ -f calculators/run_calculator_smoke_tests.sh ]; then cd calculators && bash run_calculator_smoke_tests.sh; else echo "calculator smoke tests not found."; fi

python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/power_series/cli.py --output-dir outputs; else echo "python3 not found; skipping Python workflow."; fi

r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/power_series_approximation_audit.R; else echo "Rscript not found; skipping R workflow."; fi

julia:
	@if command -v julia >/dev/null 2>&1; then julia julia/power_series_approximation_audit.jl > outputs/tables/julia_power_series_approximation_audit.csv; else echo "julia not found; skipping Julia workflow."; fi

sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/power_series.sqlite < sql/schema.sql; sqlite3 outputs/tables/power_series.sqlite < sql/analysis_queries.sql > outputs/tables/sql_power_series_report.txt; else echo "sqlite3 not found; skipping SQL workflow."; fi

haskell:
	$(MAKE) -C haskell run

c:
	@if command -v cc >/dev/null 2>&1; then cc -O2 -std=c11 c/power_series_audit.c -lm -o outputs/power_series_c; ./outputs/power_series_c > outputs/tables/c_power_series_approximation_audit.csv; else echo "cc not found; skipping C workflow."; fi

cpp:
	$(MAKE) -C cpp run

fortran:
	@if command -v gfortran >/dev/null 2>&1; then gfortran -O2 fortran/power_series_audit.f90 -o outputs/power_series_fortran; ./outputs/power_series_fortran > outputs/tables/fortran_power_series_approximation_audit.txt; else echo "gfortran not found; skipping Fortran workflow."; fi

rust:
	@if command -v cargo >/dev/null 2>&1; then cd rust && cargo run --quiet > ../outputs/tables/rust_power_series_approximation_audit.csv; else echo "cargo not found; skipping Rust workflow."; fi

go:
	@if command -v go >/dev/null 2>&1; then cd go && go run main.go > ../outputs/tables/go_power_series_approximation_audit.csv; else echo "go not found; skipping Go workflow."; fi

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log outputs/reports/*.md
	rm -f outputs/power_series_c outputs/power_series_fortran
	rm -f calculators/outputs/*.csv calculators/outputs/*.json calculators/outputs/*.txt
	$(MAKE) -C haskell clean || true
	$(MAKE) -C cpp clean || true
	$(MAKE) -C advanced clean || true
	cd rust && cargo clean || true
