.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/diagnostics_residuals_model_error/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/diagnostics_residuals_model_error_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/diagnostics_residuals_model_error.sqlite < sql/schema.sql
	sqlite3 outputs/tables/diagnostics_residuals_model_error.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/diagnostics_residuals_model_error.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/diagnostic_summary.f90 -o outputs/diagnostic_summary_fortran
	./outputs/diagnostic_summary_fortran > outputs/tables/fortran_diagnostic_summary.txt

c:
	cc -O2 -std=c11 c/diagnostic_summary.c -o outputs/diagnostic_summary_c -lm
	./outputs/diagnostic_summary_c > outputs/tables/c_diagnostic_summary.csv 2> outputs/logs/c_diagnostic_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/diagnostic_summary_c outputs/diagnostic_summary_cpp outputs/diagnostic_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
