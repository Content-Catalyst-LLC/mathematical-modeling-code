.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,orthogonal-decomposition-and-structured-approximation,Orthogonal Decomposition and Structured Approximation" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Orthogonal Decomposition and Structured Approximation"

python:
	@echo "Python scaffold for Orthogonal Decomposition and Structured Approximation"

test:
	@echo "Python test scaffold for Orthogonal Decomposition and Structured Approximation"

r:
	@echo "R scaffold for Orthogonal Decomposition and Structured Approximation"

julia:
	@echo "Julia scaffold for Orthogonal Decomposition and Structured Approximation"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/orthogonal-decomposition-and-structured-approximation.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Orthogonal Decomposition and Structured Approximation"

go:
	@echo "Go scaffold for Orthogonal Decomposition and Structured Approximation"

cpp:
	@echo "C++ scaffold for Orthogonal Decomposition and Structured Approximation"

fortran:
	@echo "Fortran scaffold for Orthogonal Decomposition and Structured Approximation"

c:
	@echo "C scaffold for Orthogonal Decomposition and Structured Approximation"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
