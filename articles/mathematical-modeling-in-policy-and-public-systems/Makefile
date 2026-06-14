.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/mathematical_modeling_in_policy_and_public_systems/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/mathematical_modeling_in_policy_and_public_systems_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/mathematical_modeling_in_policy_and_public_systems.sqlite < sql/schema.sql
	sqlite3 outputs/tables/mathematical_modeling_in_policy_and_public_systems.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/mathematical_modeling_in_policy_and_public_systems.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/policy_option_summary.f90 -o outputs/policy_option_summary_fortran
	./outputs/policy_option_summary_fortran > outputs/tables/fortran_policy_option_summary.txt

c:
	cc -O2 -std=c11 c/policy_option_summary.c -o outputs/policy_option_summary_c -lm
	./outputs/policy_option_summary_c > outputs/tables/c_policy_option_summary.csv 2> outputs/logs/c_policy_option_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/policy_option_summary_c outputs/policy_option_summary_cpp outputs/policy_option_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
