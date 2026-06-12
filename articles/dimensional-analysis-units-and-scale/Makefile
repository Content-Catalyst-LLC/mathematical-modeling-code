.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/dimensional_analysis_units_scale/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/dimensional_analysis_units_scale_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/dimensional_analysis_units_scale.sqlite < sql/schema.sql
	sqlite3 outputs/tables/dimensional_analysis_units_scale.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/dimensional_analysis_units_scale_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/unit_scale_resource_model.f90 -o outputs/unit_scale_resource_model_fortran
	./outputs/unit_scale_resource_model_fortran > outputs/tables/fortran_unit_scale_summary.txt

c:
	cc -O2 -std=c11 c/unit_scale_resource_model.c -o outputs/unit_scale_resource_model_c
	./outputs/unit_scale_resource_model_c > outputs/tables/c_unit_scale_summary.csv 2> outputs/logs/c_unit_scale_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/unit_scale_resource_model_c outputs/unit_scale_resource_model_cpp outputs/unit_scale_resource_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
