.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/boundary_scale_scope/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/boundary_scale_scope_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/boundary_scale_scope.sqlite < sql/schema.sql
	sqlite3 outputs/tables/boundary_scale_scope.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/boundary_scale_scope_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/boundary_resource_model.f90 -o outputs/boundary_resource_model_fortran
	./outputs/boundary_resource_model_fortran > outputs/tables/fortran_boundary_resource_summary.txt

c:
	cc -O2 -std=c11 c/boundary_resource_model.c -o outputs/boundary_resource_model_c
	./outputs/boundary_resource_model_c > outputs/tables/c_boundary_resource_summary.csv 2> outputs/logs/c_boundary_resource_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/boundary_resource_model_c outputs/boundary_resource_model_cpp outputs/boundary_resource_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
