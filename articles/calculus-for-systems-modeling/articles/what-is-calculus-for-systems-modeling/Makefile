.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c clean

all: python test r julia sql haskell rust go cpp fortran c

smoke: python test sql

python:
	python3 python/what_is_calculus_for_systems_modeling/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/sensitivity_workflow.R

julia:
	julia julia/dynamic_simulation.jl

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/what_is_calculus.sqlite < sql/schema.sql
	sqlite3 outputs/tables/what_is_calculus.sqlite < sql/analysis_queries.sql > outputs/tables/sql_model_report.txt

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/dynamic_model.f90 -o outputs/dynamic_model_fortran
	./outputs/dynamic_model_fortran > outputs/tables/fortran_dynamic_model.txt

c:
	cc -O2 -std=c11 c/dynamic_model.c -o outputs/dynamic_model_c
	./outputs/dynamic_model_c > outputs/tables/c_dynamic_model.csv

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
	rm -f outputs/dynamic_model_c outputs/dynamic_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true

.PHONY: advanced

advanced:
	$(MAKE) -C advanced smoke
