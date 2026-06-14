.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c clean

all: python test r julia sql haskell rust go cpp fortran c

smoke: python test sql

python:
	python3 python/functions_variables_mathematical_representation/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/functional_forms_review.R

julia:
	julia julia/functional_forms.jl

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/functions_variables.sqlite < sql/schema.sql
	sqlite3 outputs/tables/functions_variables.sqlite < sql/analysis_queries.sql > outputs/tables/sql_model_registry_report.txt

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/functional_forms.f90 -o outputs/functional_forms_fortran
	./outputs/functional_forms_fortran > outputs/tables/fortran_functional_forms.txt

c:
	cc -O2 -std=c11 c/functional_forms.c -lm -o outputs/functional_forms_c
	./outputs/functional_forms_c > outputs/tables/c_functional_forms.csv

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
	rm -f outputs/functional_forms_c outputs/functional_forms_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
