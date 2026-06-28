.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,scientific-computing-workflows-for-linear-algebra,Scientific Computing Workflows for Linear Algebra" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Scientific Computing Workflows for Linear Algebra"

python:
	@echo "Python scaffold for Scientific Computing Workflows for Linear Algebra"

test:
	@echo "Python test scaffold for Scientific Computing Workflows for Linear Algebra"

r:
	@echo "R scaffold for Scientific Computing Workflows for Linear Algebra"

julia:
	@echo "Julia scaffold for Scientific Computing Workflows for Linear Algebra"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/scientific-computing-workflows-for-linear-algebra.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Scientific Computing Workflows for Linear Algebra"

go:
	@echo "Go scaffold for Scientific Computing Workflows for Linear Algebra"

cpp:
	@echo "C++ scaffold for Scientific Computing Workflows for Linear Algebra"

fortran:
	@echo "Fortran scaffold for Scientific Computing Workflows for Linear Algebra"

c:
	@echo "C scaffold for Scientific Computing Workflows for Linear Algebra"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
