.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,matrices-and-the-organization-of-multivariable-systems,Matrices and the Organization of Multivariable Systems" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Matrices and the Organization of Multivariable Systems"

python:
	@echo "Python scaffold for Matrices and the Organization of Multivariable Systems"

test:
	@echo "Python test scaffold for Matrices and the Organization of Multivariable Systems"

r:
	@echo "R scaffold for Matrices and the Organization of Multivariable Systems"

julia:
	@echo "Julia scaffold for Matrices and the Organization of Multivariable Systems"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/matrices-and-the-organization-of-multivariable-systems.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Matrices and the Organization of Multivariable Systems"

go:
	@echo "Go scaffold for Matrices and the Organization of Multivariable Systems"

cpp:
	@echo "C++ scaffold for Matrices and the Organization of Multivariable Systems"

fortran:
	@echo "Fortran scaffold for Matrices and the Organization of Multivariable Systems"

c:
	@echo "C scaffold for Matrices and the Organization of Multivariable Systems"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
