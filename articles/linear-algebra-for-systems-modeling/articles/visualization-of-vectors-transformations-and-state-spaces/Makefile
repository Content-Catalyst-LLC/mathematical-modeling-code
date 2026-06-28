.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,visualization-of-vectors-transformations-and-state-spaces,Visualization of Vectors, Transformations, and State Spaces" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Visualization of Vectors, Transformations, and State Spaces"

python:
	@echo "Python scaffold for Visualization of Vectors, Transformations, and State Spaces"

test:
	@echo "Python test scaffold for Visualization of Vectors, Transformations, and State Spaces"

r:
	@echo "R scaffold for Visualization of Vectors, Transformations, and State Spaces"

julia:
	@echo "Julia scaffold for Visualization of Vectors, Transformations, and State Spaces"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/visualization-of-vectors-transformations-and-state-spaces.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Visualization of Vectors, Transformations, and State Spaces"

go:
	@echo "Go scaffold for Visualization of Vectors, Transformations, and State Spaces"

cpp:
	@echo "C++ scaffold for Visualization of Vectors, Transformations, and State Spaces"

fortran:
	@echo "Fortran scaffold for Visualization of Vectors, Transformations, and State Spaces"

c:
	@echo "C scaffold for Visualization of Vectors, Transformations, and State Spaces"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
