.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/model_comparison_and_selection/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/model_comparison_and_selection_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/model_comparison_and_selection.sqlite < sql/schema.sql
	sqlite3 outputs/tables/model_comparison_and_selection.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/model_comparison_and_selection.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/model_selection_summary.f90 -o outputs/model_selection_summary_fortran
	./outputs/model_selection_summary_fortran > outputs/tables/fortran_model_selection_summary.txt

c:
	cc -O2 -std=c11 c/model_selection_summary.c -o outputs/model_selection_summary_c -lm
	./outputs/model_selection_summary_c > outputs/tables/c_model_selection_summary.csv 2> outputs/logs/c_model_selection_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/model_selection_summary_c outputs/model_selection_summary_cpp outputs/model_selection_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
