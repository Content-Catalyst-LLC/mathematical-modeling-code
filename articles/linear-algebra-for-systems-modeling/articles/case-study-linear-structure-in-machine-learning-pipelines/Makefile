.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,case-study-linear-structure-in-machine-learning-pipelines,Case Study: Linear Structure in Machine Learning Pipelines" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Case Study: Linear Structure in Machine Learning Pipelines"

python:
	@echo "Python scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

test:
	@echo "Python test scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

r:
	@echo "R scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

julia:
	@echo "Julia scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/case-study-linear-structure-in-machine-learning-pipelines.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

go:
	@echo "Go scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

cpp:
	@echo "C++ scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

fortran:
	@echo "Fortran scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

c:
	@echo "C scaffold for Case Study: Linear Structure in Machine Learning Pipelines"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
