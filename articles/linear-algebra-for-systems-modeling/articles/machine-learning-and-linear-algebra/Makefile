.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,machine-learning-and-linear-algebra,Machine Learning and Linear Algebra" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Machine Learning and Linear Algebra"

python:
	@echo "Python scaffold for Machine Learning and Linear Algebra"

test:
	@echo "Python test scaffold for Machine Learning and Linear Algebra"

r:
	@echo "R scaffold for Machine Learning and Linear Algebra"

julia:
	@echo "Julia scaffold for Machine Learning and Linear Algebra"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/machine-learning-and-linear-algebra.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Machine Learning and Linear Algebra"

go:
	@echo "Go scaffold for Machine Learning and Linear Algebra"

cpp:
	@echo "C++ scaffold for Machine Learning and Linear Algebra"

fortran:
	@echo "Fortran scaffold for Machine Learning and Linear Algebra"

c:
	@echo "C scaffold for Machine Learning and Linear Algebra"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
