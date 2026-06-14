.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/mathematical_modeling_in_artificial_intelligence_and_data_systems/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/mathematical_modeling_in_artificial_intelligence_and_data_systems_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/mathematical_modeling_in_artificial_intelligence_and_data_systems.sqlite < sql/schema.sql
	sqlite3 outputs/tables/mathematical_modeling_in_artificial_intelligence_and_data_systems.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/mathematical_modeling_in_artificial_intelligence_and_data_systems.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/ai_candidate_governance_summary.f90 -o outputs/ai_candidate_governance_summary_fortran
	./outputs/ai_candidate_governance_summary_fortran > outputs/tables/fortran_ai_candidate_governance_summary.txt

c:
	cc -O2 -std=c11 c/ai_candidate_governance_summary.c -o outputs/ai_candidate_governance_summary_c -lm
	./outputs/ai_candidate_governance_summary_c > outputs/tables/c_ai_candidate_governance_summary.csv 2> outputs/logs/c_ai_candidate_governance_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/ai_candidate_governance_summary_c outputs/ai_candidate_governance_summary_cpp outputs/ai_candidate_governance_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
