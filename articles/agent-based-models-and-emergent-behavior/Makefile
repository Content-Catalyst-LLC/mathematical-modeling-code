.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/agent_based_models_emergent_behavior/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/agent_based_models_emergent_behavior_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/agent_based_models_emergent_behavior.sqlite < sql/schema.sql
	sqlite3 outputs/tables/agent_based_models_emergent_behavior.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/agent_based_models_emergent_behavior_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/abm_adoption_model.f90 -o outputs/abm_adoption_model_fortran
	./outputs/abm_adoption_model_fortran > outputs/tables/fortran_abm_adoption_summary.txt

c:
	cc -O2 -std=c11 c/abm_adoption_model.c -o outputs/abm_adoption_model_c
	./outputs/abm_adoption_model_c > outputs/tables/c_abm_adoption_trajectory.csv 2> outputs/logs/c_abm_adoption_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/abm_adoption_model_c outputs/abm_adoption_model_cpp outputs/abm_adoption_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
