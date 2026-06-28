.PHONY: all smoke calculators python test canvas r julia sql haskell c cpp fortran rust go advanced clean

all: python test canvas r julia sql haskell c cpp fortran rust go advanced calculators
smoke: python sql canvas advanced calculators

calculators:
	@if [ -f calculators/run_calculator_smoke_tests.sh ]; then cd calculators && bash run_calculator_smoke_tests.sh; fi
python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/inverse_recovery/cli.py --output-dir outputs; else echo "python3 not found; skipping."; fi
canvas:
	@if command -v python3 >/dev/null 2>&1; then python3 python/catalyst_canvas/cli.py --output-dir outputs; else echo "python3 not found; skipping Canvas."; fi
test:
	@if command -v python3 >/dev/null 2>&1 && python3 -c "import pytest" >/dev/null 2>&1; then python3 -m pytest python/tests; else echo "pytest not found; skipping."; fi
r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/inverse_recovery_audit.R; else echo "Rscript not found; skipping."; fi
julia:
	@if command -v julia >/dev/null 2>&1; then julia julia/inverse_recovery_audit.jl > outputs/tables/julia_inverse_recovery_audit.csv; else echo "julia not found; skipping."; fi
sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/inverse_recovery_audit.sqlite < sql/schema.sql; sqlite3 outputs/tables/inverse_recovery_audit.sqlite < sql/analysis_queries.sql > outputs/tables/sql_inverse_recovery_audit_report.txt; else echo "sqlite3 not found; skipping."; fi
haskell:
	$(MAKE) -C haskell run
c:
	@if command -v cc >/dev/null 2>&1; then cc -O2 -std=c11 c/inverse_recovery_audit.c -o outputs/inverse_recovery_audit_c; ./outputs/inverse_recovery_audit_c > outputs/tables/c_inverse_recovery_audit.csv; else echo "cc not found; skipping."; fi
cpp:
	$(MAKE) -C cpp run
fortran:
	@if command -v gfortran >/dev/null 2>&1; then gfortran -O2 fortran/inverse_recovery_audit.f90 -o outputs/inverse_recovery_audit_fortran; ./outputs/inverse_recovery_audit_fortran > outputs/tables/fortran_inverse_recovery_audit.txt; else echo "gfortran not found; skipping."; fi
rust:
	@if command -v cargo >/dev/null 2>&1; then cd rust && cargo run --quiet > ../outputs/tables/rust_inverse_recovery_audit.csv; else echo "cargo not found; skipping."; fi
go:
	@if command -v go >/dev/null 2>&1; then cd go && go run main.go > ../outputs/tables/go_inverse_recovery_audit.csv; else echo "go not found; skipping."; fi
advanced:
	$(MAKE) -C advanced smoke
clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite outputs/json/*.json outputs/logs/*.log outputs/reports/*.md outputs/inverse_recovery_audit_c outputs/inverse_recovery_audit_fortran
	rm -f calculators/outputs/*.csv calculators/outputs/*.json calculators/outputs/*.txt
	$(MAKE) -C haskell clean || true
	$(MAKE) -C cpp clean || true
	$(MAKE) -C advanced clean || true
	cd rust && cargo clean || true
