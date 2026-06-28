.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,overdetermined-systems-and-least-squares-thinking,Overdetermined Systems and Least Squares Thinking" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Overdetermined Systems and Least Squares Thinking"

python:
	@echo "Python scaffold for Overdetermined Systems and Least Squares Thinking"

test:
	@echo "Python test scaffold for Overdetermined Systems and Least Squares Thinking"

r:
	@echo "R scaffold for Overdetermined Systems and Least Squares Thinking"

julia:
	@echo "Julia scaffold for Overdetermined Systems and Least Squares Thinking"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/overdetermined-systems-and-least-squares-thinking.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Overdetermined Systems and Least Squares Thinking"

go:
	@echo "Go scaffold for Overdetermined Systems and Least Squares Thinking"

cpp:
	@echo "C++ scaffold for Overdetermined Systems and Least Squares Thinking"

fortran:
	@echo "Fortran scaffold for Overdetermined Systems and Least Squares Thinking"

c:
	@echo "C scaffold for Overdetermined Systems and Least Squares Thinking"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
