.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,linear-dynamical-systems,Linear Dynamical Systems" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Linear Dynamical Systems"

python:
	@echo "Python scaffold for Linear Dynamical Systems"

test:
	@echo "Python test scaffold for Linear Dynamical Systems"

r:
	@echo "R scaffold for Linear Dynamical Systems"

julia:
	@echo "Julia scaffold for Linear Dynamical Systems"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/linear-dynamical-systems.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Linear Dynamical Systems"

go:
	@echo "Go scaffold for Linear Dynamical Systems"

cpp:
	@echo "C++ scaffold for Linear Dynamical Systems"

fortran:
	@echo "Fortran scaffold for Linear Dynamical Systems"

c:
	@echo "C scaffold for Linear Dynamical Systems"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
