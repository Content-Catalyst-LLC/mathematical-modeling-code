.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/assumptions_model_design/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/assumptions_model_design_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/assumptions_model_design.sqlite < sql/schema.sql
	sqlite3 outputs/tables/assumptions_model_design.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/assumptions_model_design_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/resource_model.f90 -o outputs/resource_model_fortran
	./outputs/resource_model_fortran > outputs/tables/fortran_resource_summary.txt

c:
	cc -O2 -std=c11 c/resource_model.c -o outputs/resource_model_c
	./outputs/resource_model_c > outputs/tables/c_resource_summary.csv 2> outputs/logs/c_resource_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/resource_model_c outputs/resource_model_cpp outputs/resource_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
