.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,matrix-arithmetic-and-the-logic-of-combination,Matrix Arithmetic and the Logic of Combination" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Matrix Arithmetic and the Logic of Combination"

python:
	@echo "Python scaffold for Matrix Arithmetic and the Logic of Combination"

test:
	@echo "Python test scaffold for Matrix Arithmetic and the Logic of Combination"

r:
	@echo "R scaffold for Matrix Arithmetic and the Logic of Combination"

julia:
	@echo "Julia scaffold for Matrix Arithmetic and the Logic of Combination"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/matrix-arithmetic-and-the-logic-of-combination.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Matrix Arithmetic and the Logic of Combination"

go:
	@echo "Go scaffold for Matrix Arithmetic and the Logic of Combination"

cpp:
	@echo "C++ scaffold for Matrix Arithmetic and the Logic of Combination"

fortran:
	@echo "Fortran scaffold for Matrix Arithmetic and the Logic of Combination"

c:
	@echo "C scaffold for Matrix Arithmetic and the Logic of Combination"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
