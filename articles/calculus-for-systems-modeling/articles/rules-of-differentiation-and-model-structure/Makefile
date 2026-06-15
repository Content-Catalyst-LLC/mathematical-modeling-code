.PHONY: all smoke advanced python test r julia sql haskell rust go cpp fortran c clean

all: python test r julia sql haskell rust go cpp fortran c advanced

smoke: python test sql advanced

advanced:
	$(MAKE) -C advanced smoke

python:
	@if command -v python3 >/dev/null 2>&1; then python3 python/differentiation_model_structure/cli.py --output-dir outputs; else echo "python3 not found; skipping Python workflow."; fi

test:
	@if command -v python3 >/dev/null 2>&1 && python3 -c "import pytest" >/dev/null 2>&1; then python3 -m pytest python/tests; else echo "pytest not found; skipping Python tests."; fi

r:
	@if command -v Rscript >/dev/null 2>&1; then Rscript r/rule_based_sensitivity_decomposition.R; else echo "Rscript not found; skipping R workflow."; fi

julia:
	@if command -v julia >/dev/null 2>&1; then julia julia/structural_derivative_audit.jl > outputs/tables/julia_structural_derivative_audit.csv; else echo "julia not found; skipping Julia workflow."; fi

sql:
	@if command -v sqlite3 >/dev/null 2>&1; then mkdir -p outputs/tables; sqlite3 outputs/tables/differentiation_rules.sqlite < sql/schema.sql; sqlite3 outputs/tables/differentiation_rules.sqlite < sql/analysis_queries.sql > outputs/tables/sql_differentiation_rule_report.txt; else echo "sqlite3 not found; skipping SQL workflow."; fi

haskell:
	$(MAKE) -C haskell run

rust:
	@if command -v cargo >/dev/null 2>&1; then cd rust && cargo run --quiet > ../outputs/tables/rust_structural_derivative_audit.csv; else echo "cargo not found; skipping Rust workflow."; fi

go:
	@if command -v go >/dev/null 2>&1; then cd go && go run main.go > ../outputs/tables/go_structural_derivative_audit.csv; else echo "go not found; skipping Go workflow."; fi

cpp:
	$(MAKE) -C cpp run

fortran:
	@if command -v gfortran >/dev/null 2>&1; then gfortran -O2 fortran/structural_derivative_audit.f90 -o outputs/rule_audit_fortran; ./outputs/rule_audit_fortran > outputs/tables/fortran_structural_derivative_audit.txt; else echo "gfortran not found; skipping Fortran workflow."; fi

c:
	@if command -v cc >/dev/null 2>&1; then cc -O2 -std=c11 c/structural_derivative_audit.c -lm -o outputs/rule_audit_c; ./outputs/rule_audit_c > outputs/tables/c_structural_derivative_audit.csv; else echo "cc not found; skipping C workflow."; fi

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log outputs/reports/*.md
	rm -f outputs/rule_audit_c outputs/rule_audit_fortran
	$(MAKE) -C cpp clean || true
	$(MAKE) -C haskell clean || true
	$(MAKE) -C advanced clean || true
	cd rust && cargo clean || true
