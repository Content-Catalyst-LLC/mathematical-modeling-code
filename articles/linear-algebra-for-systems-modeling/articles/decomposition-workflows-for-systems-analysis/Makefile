.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,decomposition-workflows-for-systems-analysis,Decomposition Workflows for Systems Analysis" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Decomposition Workflows for Systems Analysis"

python:
	@echo "Python scaffold for Decomposition Workflows for Systems Analysis"

test:
	@echo "Python test scaffold for Decomposition Workflows for Systems Analysis"

r:
	@echo "R scaffold for Decomposition Workflows for Systems Analysis"

julia:
	@echo "Julia scaffold for Decomposition Workflows for Systems Analysis"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/decomposition-workflows-for-systems-analysis.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Decomposition Workflows for Systems Analysis"

go:
	@echo "Go scaffold for Decomposition Workflows for Systems Analysis"

cpp:
	@echo "C++ scaffold for Decomposition Workflows for Systems Analysis"

fortran:
	@echo "Fortran scaffold for Decomposition Workflows for Systems Analysis"

c:
	@echo "C scaffold for Decomposition Workflows for Systems Analysis"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
