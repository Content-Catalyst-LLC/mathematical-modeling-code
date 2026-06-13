.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/sensitivity_analysis_and_robustness/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/sensitivity_analysis_and_robustness_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/sensitivity_analysis_and_robustness.sqlite < sql/schema.sql
	sqlite3 outputs/tables/sensitivity_analysis_and_robustness.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/sensitivity_analysis_and_robustness.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/sensitivity_summary.f90 -o outputs/sensitivity_summary_fortran
	./outputs/sensitivity_summary_fortran > outputs/tables/fortran_sensitivity_summary.txt

c:
	cc -O2 -std=c11 c/sensitivity_summary.c -o outputs/sensitivity_summary_c -lm
	./outputs/sensitivity_summary_c > outputs/tables/c_sensitivity_summary.csv 2> outputs/logs/c_sensitivity_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/sensitivity_summary_c outputs/sensitivity_summary_cpp outputs/sensitivity_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
