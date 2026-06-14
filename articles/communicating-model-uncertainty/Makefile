.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/communicating_model_uncertainty/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/communicating_model_uncertainty_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/communicating_model_uncertainty.sqlite < sql/schema.sql
	sqlite3 outputs/tables/communicating_model_uncertainty.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/communicating_model_uncertainty.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/communication_summary.f90 -o outputs/communication_summary_fortran
	./outputs/communication_summary_fortran > outputs/tables/fortran_communication_summary.txt

c:
	cc -O2 -std=c11 c/communication_summary.c -o outputs/communication_summary_c -lm
	./outputs/communication_summary_c > outputs/tables/c_communication_summary.csv 2> outputs/logs/c_communication_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/communication_summary_c outputs/communication_summary_cpp outputs/communication_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
