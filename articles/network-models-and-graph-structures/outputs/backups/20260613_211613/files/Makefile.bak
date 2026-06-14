.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/network_models_graph_structures/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/network_models_graph_structures_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/network_models_graph_structures.sqlite < sql/schema.sql
	sqlite3 outputs/tables/network_models_graph_structures.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/network_models_graph_structures_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/network_graph_diagnostics.f90 -o outputs/network_graph_diagnostics_fortran
	./outputs/network_graph_diagnostics_fortran > outputs/tables/fortran_network_diagnostics.txt

c:
	cc -O2 -std=c11 c/network_graph_diagnostics.c -o outputs/network_graph_diagnostics_c
	./outputs/network_graph_diagnostics_c > outputs/tables/c_network_node_diagnostics.csv 2> outputs/logs/c_network_graph_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/network_graph_diagnostics_c outputs/network_graph_diagnostics_cpp outputs/network_graph_diagnostics_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
