.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,what-is-linear-algebra-for-systems-modeling,What Is Linear Algebra for Systems Modeling?" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for What Is Linear Algebra for Systems Modeling?"

python:
	@echo "Python scaffold for What Is Linear Algebra for Systems Modeling?"

test:
	@echo "Python test scaffold for What Is Linear Algebra for Systems Modeling?"

r:
	@echo "R scaffold for What Is Linear Algebra for Systems Modeling?"

julia:
	@echo "Julia scaffold for What Is Linear Algebra for Systems Modeling?"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/what-is-linear-algebra-for-systems-modeling.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for What Is Linear Algebra for Systems Modeling?"

go:
	@echo "Go scaffold for What Is Linear Algebra for Systems Modeling?"

cpp:
	@echo "C++ scaffold for What Is Linear Algebra for Systems Modeling?"

fortran:
	@echo "Fortran scaffold for What Is Linear Algebra for Systems Modeling?"

c:
	@echo "C scaffold for What Is Linear Algebra for Systems Modeling?"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
