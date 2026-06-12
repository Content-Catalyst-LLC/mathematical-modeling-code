.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/model_repositories_reproducible_research/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/model_repositories_reproducible_research_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/model_repositories_reproducible_research.sqlite < sql/schema.sql
	sqlite3 outputs/tables/model_repositories_reproducible_research.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/model_repositories_reproducible_research.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/repository_inventory_summary.f90 -o outputs/repository_inventory_summary_fortran
	./outputs/repository_inventory_summary_fortran > outputs/tables/fortran_repository_inventory_summary.txt

c:
	cc -O2 -std=c11 c/repository_inventory_summary.c -o outputs/repository_inventory_summary_c
	./outputs/repository_inventory_summary_c > outputs/tables/c_repository_inventory_summary.csv 2> outputs/logs/c_repository_inventory_summary_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/repository_inventory_summary_c outputs/repository_inventory_summary_cpp outputs/repository_inventory_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
