.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/model_governance_and_accountability/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/model_governance_and_accountability_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/model_governance_and_accountability.sqlite < sql/schema.sql
	sqlite3 outputs/tables/model_governance_and_accountability.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/model_governance_and_accountability.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/governance_risk_summary.f90 -o outputs/governance_risk_summary_fortran
	./outputs/governance_risk_summary_fortran > outputs/tables/fortran_governance_risk_summary.txt

c:
	cc -O2 -std=c11 c/governance_risk_summary.c -o outputs/governance_risk_summary_c -lm
	./outputs/governance_risk_summary_c > outputs/tables/c_governance_risk_summary.csv 2> outputs/logs/c_governance_risk_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/governance_risk_summary_c outputs/governance_risk_summary_cpp outputs/governance_risk_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
