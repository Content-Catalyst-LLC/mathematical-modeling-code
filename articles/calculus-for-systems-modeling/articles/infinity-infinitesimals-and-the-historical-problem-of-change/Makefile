.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c clean

all: python test r julia sql haskell rust go cpp fortran c

smoke: python test sql

python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/infinity_infinitesimals_change/cli.py --output-dir outputs; else echo "python3 not found; skipping Python workflow."; fi

test:
	@if command -v python3 >/dev/null 2>&1 && python3 -c "import pytest" >/dev/null 2>&1; then python3 -m pytest python/tests; else echo "pytest not found; skipping Python tests."; fi

r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/difference_quotient_convergence.R; else echo "Rscript not found; skipping R workflow."; fi

julia:
	@if command -v julia >/dev/null 2>&1; then julia julia/difference_quotient_convergence.jl; else echo "julia not found; skipping Julia workflow."; fi

sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/infinity_infinitesimals.sqlite < sql/schema.sql; sqlite3 outputs/tables/infinity_infinitesimals.sqlite < sql/analysis_queries.sql > outputs/tables/sql_concept_registry_report.txt; else echo "sqlite3 not found; skipping SQL workflow."; fi

haskell:
	$(MAKE) -C haskell run

rust:
	@if command -v cargo >/dev/null 2>&1; then cd rust && cargo run --quiet; else echo "cargo not found; skipping Rust workflow."; fi

go:
	@if command -v go >/dev/null 2>&1; then cd go && go run main.go; else echo "go not found; skipping Go workflow."; fi

cpp:
	$(MAKE) -C cpp run

fortran:
	@if command -v gfortran >/dev/null 2>&1; then gfortran -O2 fortran/difference_quotient.f90 -o outputs/difference_quotient_fortran; ./outputs/difference_quotient_fortran > outputs/tables/fortran_difference_quotient.txt; else echo "gfortran not found; skipping Fortran workflow."; fi

c:
	@if command -v cc >/dev/null 2>&1; then cc -O2 -std=c11 c/difference_quotient.c -lm -o outputs/difference_quotient_c; ./outputs/difference_quotient_c > outputs/tables/c_difference_quotient.csv; else echo "cc not found; skipping C workflow."; fi

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
	rm -f outputs/difference_quotient_c outputs/difference_quotient_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true

.PHONY: advanced

advanced:
	$(MAKE) -C advanced smoke
