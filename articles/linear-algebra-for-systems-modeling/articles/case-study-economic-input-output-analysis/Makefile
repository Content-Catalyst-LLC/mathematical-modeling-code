.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,case-study-economic-input-output-analysis,Case Study: Economic Input-Output Analysis" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Case Study: Economic Input-Output Analysis"

python:
	@echo "Python scaffold for Case Study: Economic Input-Output Analysis"

test:
	@echo "Python test scaffold for Case Study: Economic Input-Output Analysis"

r:
	@echo "R scaffold for Case Study: Economic Input-Output Analysis"

julia:
	@echo "Julia scaffold for Case Study: Economic Input-Output Analysis"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/case-study-economic-input-output-analysis.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Case Study: Economic Input-Output Analysis"

go:
	@echo "Go scaffold for Case Study: Economic Input-Output Analysis"

cpp:
	@echo "C++ scaffold for Case Study: Economic Input-Output Analysis"

fortran:
	@echo "Fortran scaffold for Case Study: Economic Input-Output Analysis"

c:
	@echo "C scaffold for Case Study: Economic Input-Output Analysis"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
