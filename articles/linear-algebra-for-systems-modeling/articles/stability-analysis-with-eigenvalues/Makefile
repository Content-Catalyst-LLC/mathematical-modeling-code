.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,stability-analysis-with-eigenvalues,Stability Analysis with Eigenvalues" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Stability Analysis with Eigenvalues"

python:
	@echo "Python scaffold for Stability Analysis with Eigenvalues"

test:
	@echo "Python test scaffold for Stability Analysis with Eigenvalues"

r:
	@echo "R scaffold for Stability Analysis with Eigenvalues"

julia:
	@echo "Julia scaffold for Stability Analysis with Eigenvalues"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/stability-analysis-with-eigenvalues.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Stability Analysis with Eigenvalues"

go:
	@echo "Go scaffold for Stability Analysis with Eigenvalues"

cpp:
	@echo "C++ scaffold for Stability Analysis with Eigenvalues"

fortran:
	@echo "Fortran scaffold for Stability Analysis with Eigenvalues"

c:
	@echo "C scaffold for Stability Analysis with Eigenvalues"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
