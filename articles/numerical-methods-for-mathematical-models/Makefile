.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/numerical_methods_for_mathematical_models/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/numerical_methods_for_mathematical_models_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/numerical_methods_for_mathematical_models.sqlite < sql/schema.sql
	sqlite3 outputs/tables/numerical_methods_for_mathematical_models.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/numerical_methods_for_mathematical_models_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/euler_resource_model.f90 -o outputs/euler_resource_model_fortran
	./outputs/euler_resource_model_fortran > outputs/tables/fortran_euler_resource_trajectory.txt

c:
	cc -O2 -std=c11 c/euler_resource_model.c -o outputs/euler_resource_model_c
	./outputs/euler_resource_model_c > outputs/tables/c_euler_resource_trajectory.csv 2> outputs/logs/c_euler_resource_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/euler_resource_model_c outputs/euler_resource_model_cpp outputs/euler_resource_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
