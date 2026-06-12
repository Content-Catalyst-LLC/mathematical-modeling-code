.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/spatial_models_geometric_representation/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/spatial_models_geometric_representation_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/spatial_models_geometric_representation.sqlite < sql/schema.sql
	sqlite3 outputs/tables/spatial_models_geometric_representation.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/spatial_models_geometric_representation_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/spatial_distance_diagnostics.f90 -o outputs/spatial_distance_diagnostics_fortran
	./outputs/spatial_distance_diagnostics_fortran > outputs/tables/fortran_spatial_distance_diagnostics.txt

c:
	cc -O2 -std=c11 c/spatial_distance_diagnostics.c -lm -o outputs/spatial_distance_diagnostics_c
	./outputs/spatial_distance_diagnostics_c > outputs/tables/c_spatial_distance_diagnostics.csv 2> outputs/logs/c_spatial_distance_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/spatial_distance_diagnostics_c outputs/spatial_distance_diagnostics_cpp outputs/spatial_distance_diagnostics_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
