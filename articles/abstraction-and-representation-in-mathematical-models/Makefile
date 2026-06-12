.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/abstraction_representation/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/abstraction_representation_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/abstraction_representation.sqlite < sql/schema.sql
	sqlite3 outputs/tables/abstraction_representation.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/abstraction_representation_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/stock_flow_model.f90 -o outputs/stock_flow_model_fortran
	./outputs/stock_flow_model_fortran > outputs/tables/fortran_stock_flow_summary.txt

c:
	cc -O2 -std=c11 c/stock_flow_model.c -o outputs/stock_flow_model_c
	./outputs/stock_flow_model_c > outputs/tables/c_stock_flow_summary.csv 2> outputs/logs/c_stock_flow_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/stock_flow_model_c outputs/stock_flow_model_cpp outputs/stock_flow_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
