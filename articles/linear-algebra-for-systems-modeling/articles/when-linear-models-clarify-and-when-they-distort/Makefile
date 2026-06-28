.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,when-linear-models-clarify-and-when-they-distort,When Linear Models Clarify and When They Distort" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for When Linear Models Clarify and When They Distort"

python:
	@echo "Python scaffold for When Linear Models Clarify and When They Distort"

test:
	@echo "Python test scaffold for When Linear Models Clarify and When They Distort"

r:
	@echo "R scaffold for When Linear Models Clarify and When They Distort"

julia:
	@echo "Julia scaffold for When Linear Models Clarify and When They Distort"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/when-linear-models-clarify-and-when-they-distort.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for When Linear Models Clarify and When They Distort"

go:
	@echo "Go scaffold for When Linear Models Clarify and When They Distort"

cpp:
	@echo "C++ scaffold for When Linear Models Clarify and When They Distort"

fortran:
	@echo "Fortran scaffold for When Linear Models Clarify and When They Distort"

c:
	@echo "C scaffold for When Linear Models Clarify and When They Distort"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
