.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/scientific_computing_modeling_workflows/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/scientific_computing_modeling_workflows_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/scientific_computing_modeling_workflows.sqlite < sql/schema.sql
	sqlite3 outputs/tables/scientific_computing_modeling_workflows.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/scientific_computing_modeling_workflows.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/workflow_resource_model.f90 -o outputs/workflow_resource_model_fortran
	./outputs/workflow_resource_model_fortran > outputs/tables/fortran_workflow_resource_model.txt

c:
	cc -O2 -std=c11 c/workflow_resource_model.c -o outputs/workflow_resource_model_c
	./outputs/workflow_resource_model_c > outputs/tables/c_workflow_resource_model.csv 2> outputs/logs/c_workflow_resource_model_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/workflow_resource_model_c outputs/workflow_resource_model_cpp outputs/workflow_resource_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
