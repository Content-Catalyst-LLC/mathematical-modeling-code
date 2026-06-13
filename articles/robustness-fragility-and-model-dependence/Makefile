.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/robustness_fragility_and_model_dependence/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/robustness_fragility_and_model_dependence_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/robustness_fragility_and_model_dependence.sqlite < sql/schema.sql
	sqlite3 outputs/tables/robustness_fragility_and_model_dependence.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/robustness_fragility_and_model_dependence.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/robustness_summary.f90 -o outputs/robustness_summary_fortran
	./outputs/robustness_summary_fortran > outputs/tables/fortran_robustness_summary.txt

c:
	cc -O2 -std=c11 c/robustness_summary.c -o outputs/robustness_summary_c -lm
	./outputs/robustness_summary_c > outputs/tables/c_robustness_summary.csv 2> outputs/logs/c_robustness_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/robustness_summary_c outputs/robustness_summary_cpp outputs/robustness_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
