.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/structural_uncertainty_and_model_form_error/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/structural_uncertainty_and_model_form_error_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/structural_uncertainty_and_model_form_error.sqlite < sql/schema.sql
	sqlite3 outputs/tables/structural_uncertainty_and_model_form_error.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/structural_uncertainty_and_model_form_error.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/structural_summary.f90 -o outputs/structural_summary_fortran
	./outputs/structural_summary_fortran > outputs/tables/fortran_structural_summary.txt

c:
	cc -O2 -std=c11 c/structural_summary.c -o outputs/structural_summary_c -lm
	./outputs/structural_summary_c > outputs/tables/c_structural_summary.csv 2> outputs/logs/c_structural_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/structural_summary_c outputs/structural_summary_cpp outputs/structural_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
