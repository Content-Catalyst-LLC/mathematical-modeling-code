.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/algebraic_models_static_relationships/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/algebraic_models_static_relationships_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/algebraic_models_static_relationships.sqlite < sql/schema.sql
	sqlite3 outputs/tables/algebraic_models_static_relationships.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/algebraic_models_static_relationships_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/static_allocation_model.f90 -o outputs/static_allocation_model_fortran
	./outputs/static_allocation_model_fortran > outputs/tables/fortran_static_allocation_summary.txt

c:
	cc -O2 -std=c11 c/static_allocation_model.c -o outputs/static_allocation_model_c
	./outputs/static_allocation_model_c > outputs/tables/c_static_allocation_summary.csv 2> outputs/logs/c_static_allocation_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/static_allocation_model_c outputs/static_allocation_model_cpp outputs/static_allocation_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
