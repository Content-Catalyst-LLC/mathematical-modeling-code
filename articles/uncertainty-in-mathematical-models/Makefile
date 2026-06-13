.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/uncertainty_in_mathematical_models/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/uncertainty_in_mathematical_models_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/uncertainty_in_mathematical_models.sqlite < sql/schema.sql
	sqlite3 outputs/tables/uncertainty_in_mathematical_models.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/uncertainty_in_mathematical_models.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/uncertainty_summary.f90 -o outputs/uncertainty_summary_fortran
	./outputs/uncertainty_summary_fortran > outputs/tables/fortran_uncertainty_summary.txt

c:
	cc -O2 -std=c11 c/uncertainty_summary.c -o outputs/uncertainty_summary_c -lm
	./outputs/uncertainty_summary_c > outputs/tables/c_uncertainty_summary.csv 2> outputs/logs/c_uncertainty_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/uncertainty_summary_c outputs/uncertainty_summary_cpp outputs/uncertainty_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
