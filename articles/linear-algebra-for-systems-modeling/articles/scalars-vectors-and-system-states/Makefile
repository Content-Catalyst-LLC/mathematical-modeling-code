.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,scalars-vectors-and-system-states,Scalars, Vectors, and System States" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Scalars, Vectors, and System States"

python:
	@echo "Python scaffold for Scalars, Vectors, and System States"

test:
	@echo "Python test scaffold for Scalars, Vectors, and System States"

r:
	@echo "R scaffold for Scalars, Vectors, and System States"

julia:
	@echo "Julia scaffold for Scalars, Vectors, and System States"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/scalars-vectors-and-system-states.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Scalars, Vectors, and System States"

go:
	@echo "Go scaffold for Scalars, Vectors, and System States"

cpp:
	@echo "C++ scaffold for Scalars, Vectors, and System States"

fortran:
	@echo "Fortran scaffold for Scalars, Vectors, and System States"

c:
	@echo "C scaffold for Scalars, Vectors, and System States"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
