.PHONY: all available smoke python test r sql julia haskell rust go cpp fortran c clean

all: python r sql julia haskell rust go cpp fortran c

available:
	@echo "Run individual targets based on installed tools: python, r, sql, julia, haskell, rust, go, cpp, fortran, c"

smoke: python sql

python:
	python3 python/calibration_estimation_parameter_fitting/cli.py --output-dir outputs

test:
	python3 -m pytest python/tests

r:
	Rscript r/calibration_estimation_parameter_fitting_review.R

sql:
	mkdir -p outputs/tables
	sqlite3 outputs/tables/calibration_estimation_parameter_fitting.sqlite < sql/schema.sql
	sqlite3 outputs/tables/calibration_estimation_parameter_fitting.sqlite < sql/analysis_queries.sql > outputs/tables/sql_diagnostic_report.txt

julia:
	julia julia/calibration_estimation_parameter_fitting.jl

haskell:
	$(MAKE) -C haskell run

rust:
	cd rust && cargo run --quiet

go:
	cd go && go run main.go

cpp:
	$(MAKE) -C cpp run

fortran:
	gfortran -O2 fortran/calibration_resource_fit.f90 -o outputs/calibration_resource_fit_fortran
	./outputs/calibration_resource_fit_fortran > outputs/tables/fortran_calibration_summary.txt

c:
	cc -O2 -std=c11 c/calibration_resource_fit.c -o outputs/calibration_resource_fit_c -lm
	./outputs/calibration_resource_fit_c > outputs/tables/c_calibration_summary.csv 2> outputs/logs/c_calibration_stderr.log

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/figures/*.png
	rm -f outputs/calibration_resource_fit_c outputs/calibration_resource_fit_cpp outputs/calibration_resource_fit_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true
