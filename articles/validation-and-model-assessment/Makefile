.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/validation_and_model_assessment/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/validation_and_model_assessment_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/validation_and_model_assessment.sqlite < sql/schema.sql
	sqlite3 outputs/tables/validation_and_model_assessment.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/validation_and_model_assessment.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/validation_error_summary.f90 -o outputs/validation_error_summary_fortran
	./outputs/validation_error_summary_fortran > outputs/tables/fortran_validation_summary.txt

c:
	cc -O2 -std=c11 c/validation_error_summary.c -o outputs/validation_error_summary_c -lm
	./outputs/validation_error_summary_c > outputs/tables/c_validation_summary.csv 2> outputs/logs/c_validation_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/validation_error_summary_c outputs/validation_error_summary_cpp outputs/validation_error_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
