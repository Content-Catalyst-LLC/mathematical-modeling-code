.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,systems-of-linear-equations,Systems of Linear Equations" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Systems of Linear Equations"

python:
	@echo "Python scaffold for Systems of Linear Equations"

test:
	@echo "Python test scaffold for Systems of Linear Equations"

r:
	@echo "R scaffold for Systems of Linear Equations"

julia:
	@echo "Julia scaffold for Systems of Linear Equations"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/systems-of-linear-equations.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Systems of Linear Equations"

go:
	@echo "Go scaffold for Systems of Linear Equations"

cpp:
	@echo "C++ scaffold for Systems of Linear Equations"

fortran:
	@echo "Fortran scaffold for Systems of Linear Equations"

c:
	@echo "C scaffold for Systems of Linear Equations"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
