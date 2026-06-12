.PHONY: all python test r sql julia haskell rust go cpp fortran c clean smoke

all: python r sql julia haskell rust go cpp fortran c

python:
	python3 python/modeling_process/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/modeling_process_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/modeling_process.sqlite < sql/schema.sql
	sqlite3 outputs/tables/modeling_process.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/modeling_process_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run .

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/reservoir_model.f90 -o outputs/reservoir_model_fortran
	./outputs/reservoir_model_fortran > outputs/tables/fortran_reservoir_summary.txt

c:
	cc -O2 -std=c11 c/reservoir_model.c -o outputs/reservoir_model_c
	./outputs/reservoir_model_c > outputs/tables/c_reservoir_summary.csv

smoke: python sql

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.dot
	rm -f outputs/reservoir_model_c outputs/reservoir_model_cpp outputs/reservoir_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
