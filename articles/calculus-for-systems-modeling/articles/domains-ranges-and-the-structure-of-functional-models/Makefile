.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c clean

all: python test r julia sql haskell rust go cpp fortran c
smoke: python test sql

python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/domains_ranges_functional_models/cli.py --output-dir outputs; else echo "python3 not found; skipping."; fi

test:
	@if command -v python3 >/dev/null 2>&1 && python3 -c "import pytest" >/dev/null 2>&1; then python3 -m pytest python/tests; else echo "pytest not found; skipping."; fi

r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/domain_range_validation.R; else echo "Rscript not found; skipping."; fi

julia:
	@if command -v julia >/dev/null 2>&1; then julia julia/domain_range_validation.jl; else echo "julia not found; skipping."; fi

sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/domains_ranges.sqlite < sql/schema.sql; sqlite3 outputs/tables/domains_ranges.sqlite < sql/analysis_queries.sql > outputs/tables/sql_domain_range_report.txt; else echo "sqlite3 not found; skipping."; fi

haskell:
	$(MAKE) -C haskell run

rust:
	@if command -v cargo >/dev/null 2>&1; then cd rust && cargo run --quiet; else echo "cargo not found; skipping."; fi

go:
	@if command -v go >/dev/null 2>&1; then cd go && go run main.go; else echo "go not found; skipping."; fi

cpp:
	$(MAKE) -C cpp run

fortran:
	@if command -v gfortran >/dev/null 2>&1; then mkdir -p outputs/tables; gfortran -O2 fortran/domain_range_validation.f90 -o outputs/domain_range_fortran; ./outputs/domain_range_fortran > outputs/tables/fortran_domain_range_validation.txt; else echo "gfortran not found; skipping."; fi

c:
	@if command -v cc >/dev/null 2>&1; then mkdir -p outputs/tables; cc -O2 -std=c11 c/domain_range_validation.c -lm -o outputs/domain_range_c; ./outputs/domain_range_c > outputs/tables/c_domain_range_validation.csv; else echo "cc not found; skipping."; fi

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite outputs/json/*.json outputs/logs/*.log outputs/domain_range_c outputs/domain_range_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	cd rust && cargo clean || true

.PHONY: advanced

advanced:
	$(MAKE) -C advanced smoke
