.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,case-study-dimensionality-reduction-in-high-dimensional-data,Case Study: Dimensionality Reduction in High-Dimensional Data" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Case Study: Dimensionality Reduction in High-Dimensional Data"

python:
	@echo "Python scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

test:
	@echo "Python test scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

r:
	@echo "R scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

julia:
	@echo "Julia scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/case-study-dimensionality-reduction-in-high-dimensional-data.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

go:
	@echo "Go scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

cpp:
	@echo "C++ scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

fortran:
	@echo "Fortran scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

c:
	@echo "C scaffold for Case Study: Dimensionality Reduction in High-Dimensional Data"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
