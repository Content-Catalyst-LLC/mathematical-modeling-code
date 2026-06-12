.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/probabilistic_stochastic_models/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/probabilistic_stochastic_models_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/probabilistic_stochastic_models.sqlite < sql/schema.sql
	sqlite3 outputs/tables/probabilistic_stochastic_models.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/probabilistic_stochastic_models_workflow.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/probabilistic_risk_model.f90 -o outputs/probabilistic_risk_model_fortran
	./outputs/probabilistic_risk_model_fortran > outputs/tables/fortran_probabilistic_risk_summary.txt

c:
	cc -O2 -std=c11 c/probabilistic_risk_model.c -lm -o outputs/probabilistic_risk_model_c
	./outputs/probabilistic_risk_model_c > outputs/tables/c_probabilistic_risk_runs.csv 2> outputs/logs/c_probabilistic_risk_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png outputs/figures/*.dot
	rm -f outputs/probabilistic_risk_model_c outputs/probabilistic_risk_model_cpp outputs/probabilistic_risk_model_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
