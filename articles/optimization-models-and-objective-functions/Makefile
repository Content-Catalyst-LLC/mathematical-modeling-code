.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/optimization_models_objective_functions/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/optimization_models_objective_functions_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/optimization_models_objective_functions.sqlite < sql/schema.sql
	sqlite3 outputs/tables/optimization_models_objective_functions.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/optimization_models_objective_functions_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/optimization_allocation_model.f90 -o outputs/optimization_allocation_model_fortran
	./outputs/optimization_allocation_model_fortran > outputs/tables/fortran_optimization_allocation_summary.txt

c:
	cc -O2 -std=c11 c/optimization_allocation_model.c -o outputs/optimization_allocation_model_c
	./outputs/optimization_allocation_model_c > outputs/tables/c_optimization_allocation_candidates.csv 2> outputs/logs/c_optimization_allocation_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/optimization_allocation_model_c outputs/optimization_allocation_model_cpp outputs/optimization_allocation_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
