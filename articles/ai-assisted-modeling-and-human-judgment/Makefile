.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/ai_assisted_modeling_and_human_judgment/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/ai_assisted_modeling_and_human_judgment_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/ai_assisted_modeling_and_human_judgment.sqlite < sql/schema.sql
	sqlite3 outputs/tables/ai_assisted_modeling_and_human_judgment.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/ai_assisted_modeling_and_human_judgment.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/human_judgment_risk_summary.f90 -o outputs/human_judgment_risk_summary_fortran
	./outputs/human_judgment_risk_summary_fortran > outputs/tables/fortran_human_judgment_risk_summary.txt

c:
	cc -O2 -std=c11 c/human_judgment_risk_summary.c -o outputs/human_judgment_risk_summary_c -lm
	./outputs/human_judgment_risk_summary_c > outputs/tables/c_human_judgment_risk_summary.csv 2> outputs/logs/c_human_judgment_risk_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/human_judgment_risk_summary_c outputs/human_judgment_risk_summary_cpp outputs/human_judgment_risk_summary_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
