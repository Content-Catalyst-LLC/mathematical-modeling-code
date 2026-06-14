.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/limits_failure_and_the_ethics_of_modeling/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/limits_failure_and_the_ethics_of_modeling_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/limits_failure_and_the_ethics_of_modeling.sqlite < sql/schema.sql
	sqlite3 outputs/tables/limits_failure_and_the_ethics_of_modeling.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/limits_failure_and_the_ethics_of_modeling.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/model_ethics_risk_summary.f90 -o outputs/model_ethics_risk_summary_fortran
	./outputs/model_ethics_risk_summary_fortran > outputs/tables/fortran_model_ethics_risk_summary.txt

c:
	cc -O2 -std=c11 c/model_ethics_risk_summary.c -o outputs/model_ethics_risk_summary_c -lm
	./outputs/model_ethics_risk_summary_c > outputs/tables/c_model_ethics_risk_summary.csv 2> outputs/logs/c_model_ethics_risk_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/model_ethics_risk_summary_c outputs/model_ethics_risk_summary_cpp outputs/model_ethics_risk_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
