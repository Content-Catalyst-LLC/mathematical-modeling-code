.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,dimension-and-the-structure-of-solution-spaces,Dimension and the Structure of Solution Spaces" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Dimension and the Structure of Solution Spaces"

python:
	@echo "Python scaffold for Dimension and the Structure of Solution Spaces"

test:
	@echo "Python test scaffold for Dimension and the Structure of Solution Spaces"

r:
	@echo "R scaffold for Dimension and the Structure of Solution Spaces"

julia:
	@echo "Julia scaffold for Dimension and the Structure of Solution Spaces"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/dimension-and-the-structure-of-solution-spaces.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Dimension and the Structure of Solution Spaces"

go:
	@echo "Go scaffold for Dimension and the Structure of Solution Spaces"

cpp:
	@echo "C++ scaffold for Dimension and the Structure of Solution Spaces"

fortran:
	@echo "Fortran scaffold for Dimension and the Structure of Solution Spaces"

c:
	@echo "C scaffold for Dimension and the Structure of Solution Spaces"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
