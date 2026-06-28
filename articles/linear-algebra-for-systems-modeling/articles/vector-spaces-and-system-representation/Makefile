.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,vector-spaces-and-system-representation,Vector Spaces and System Representation" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Vector Spaces and System Representation"

python:
	@echo "Python scaffold for Vector Spaces and System Representation"

test:
	@echo "Python test scaffold for Vector Spaces and System Representation"

r:
	@echo "R scaffold for Vector Spaces and System Representation"

julia:
	@echo "Julia scaffold for Vector Spaces and System Representation"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/vector-spaces-and-system-representation.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Vector Spaces and System Representation"

go:
	@echo "Go scaffold for Vector Spaces and System Representation"

cpp:
	@echo "C++ scaffold for Vector Spaces and System Representation"

fortran:
	@echo "Fortran scaffold for Vector Spaces and System Representation"

c:
	@echo "C scaffold for Vector Spaces and System Representation"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
