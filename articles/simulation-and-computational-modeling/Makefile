.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/simulation_computational_modeling/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/simulation_computational_modeling_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/simulation_computational_modeling.sqlite < sql/schema.sql
	sqlite3 outputs/tables/simulation_computational_modeling.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/simulation_computational_modeling_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/resource_simulation.f90 -o outputs/resource_simulation_fortran
	./outputs/resource_simulation_fortran > outputs/tables/fortran_resource_simulation.txt

c:
	cc -O2 -std=c11 c/resource_simulation.c -o outputs/resource_simulation_c
	./outputs/resource_simulation_c > outputs/tables/c_resource_simulation.csv 2> outputs/logs/c_resource_simulation_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/resource_simulation_c outputs/resource_simulation_cpp outputs/resource_simulation_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
