.PHONY: all smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c
smoke: python sql

python:
	python3 python/variables_parameters_constraints/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/variables_parameters_constraints_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/variables_parameters_constraints.sqlite < sql/schema.sql
	sqlite3 outputs/tables/variables_parameters_constraints.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/variables_parameters_constraints_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/component_resource_model.f90 -o outputs/component_resource_model_fortran
	./outputs/component_resource_model_fortran > outputs/tables/fortran_component_resource_summary.txt

c:
	cc -O2 -std=c11 c/component_resource_model.c -o outputs/component_resource_model_c
	./outputs/component_resource_model_c > outputs/tables/c_component_resource_summary.csv 2> outputs/logs/c_component_resource_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/component_resource_model_*
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
