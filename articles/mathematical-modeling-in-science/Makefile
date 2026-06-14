.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/mathematical_modeling_in_science/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/mathematical_modeling_in_science_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/mathematical_modeling_in_science.sqlite < sql/schema.sql
	sqlite3 outputs/tables/mathematical_modeling_in_science.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/mathematical_modeling_in_science.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/population_science_summary.f90 -o outputs/population_science_summary_fortran
	./outputs/population_science_summary_fortran > outputs/tables/fortran_population_science_summary.txt

c:
	cc -O2 -std=c11 c/population_science_summary.c -o outputs/population_science_summary_c -lm
	./outputs/population_science_summary_c > outputs/tables/c_population_science_summary.csv 2> outputs/logs/c_population_science_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/population_science_summary_c outputs/population_science_summary_cpp outputs/population_science_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
