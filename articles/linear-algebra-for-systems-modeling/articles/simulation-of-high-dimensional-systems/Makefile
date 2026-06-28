.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,simulation-of-high-dimensional-systems,Simulation of High-Dimensional Systems" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Simulation of High-Dimensional Systems"

python:
	@echo "Python scaffold for Simulation of High-Dimensional Systems"

test:
	@echo "Python test scaffold for Simulation of High-Dimensional Systems"

r:
	@echo "R scaffold for Simulation of High-Dimensional Systems"

julia:
	@echo "Julia scaffold for Simulation of High-Dimensional Systems"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/simulation-of-high-dimensional-systems.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Simulation of High-Dimensional Systems"

go:
	@echo "Go scaffold for Simulation of High-Dimensional Systems"

cpp:
	@echo "C++ scaffold for Simulation of High-Dimensional Systems"

fortran:
	@echo "Fortran scaffold for Simulation of High-Dimensional Systems"

c:
	@echo "C scaffold for Simulation of High-Dimensional Systems"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
