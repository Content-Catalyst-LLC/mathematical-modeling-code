.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,reproducible-linear-algebra-workflows-with-notebooks-and-documentation,Reproducible Linear Algebra Workflows with Notebooks and Documentation" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

python:
	@echo "Python scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

test:
	@echo "Python test scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

r:
	@echo "R scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

julia:
	@echo "Julia scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/reproducible-linear-algebra-workflows-with-notebooks-and-documentation.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

go:
	@echo "Go scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

cpp:
	@echo "C++ scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

fortran:
	@echo "Fortran scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

c:
	@echo "C scaffold for Reproducible Linear Algebra Workflows with Notebooks and Documentation"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
