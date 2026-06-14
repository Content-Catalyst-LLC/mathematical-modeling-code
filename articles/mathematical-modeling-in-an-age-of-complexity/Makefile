.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/mathematical_modeling_in_an_age_of_complexity/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/mathematical_modeling_in_an_age_of_complexity_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/mathematical_modeling_in_an_age_of_complexity.sqlite < sql/schema.sql
	sqlite3 outputs/tables/mathematical_modeling_in_an_age_of_complexity.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/mathematical_modeling_in_an_age_of_complexity.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/complexity_scenario_summary.f90 -o outputs/complexity_scenario_summary_fortran
	./outputs/complexity_scenario_summary_fortran > outputs/tables/fortran_complexity_scenario_summary.txt

c:
	cc -O2 -std=c11 c/complexity_scenario_summary.c -o outputs/complexity_scenario_summary_c -lm
	./outputs/complexity_scenario_summary_c > outputs/tables/c_complexity_scenario_summary.csv 2> outputs/logs/c_complexity_scenario_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/complexity_scenario_summary_c outputs/complexity_scenario_summary_cpp outputs/complexity_scenario_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
