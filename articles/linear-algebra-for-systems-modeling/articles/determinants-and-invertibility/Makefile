.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,determinants-and-invertibility,Determinants and Invertibility" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Determinants and Invertibility"

python:
	@echo "Python scaffold for Determinants and Invertibility"

test:
	@echo "Python test scaffold for Determinants and Invertibility"

r:
	@echo "R scaffold for Determinants and Invertibility"

julia:
	@echo "Julia scaffold for Determinants and Invertibility"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/determinants-and-invertibility.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Determinants and Invertibility"

go:
	@echo "Go scaffold for Determinants and Invertibility"

cpp:
	@echo "C++ scaffold for Determinants and Invertibility"

fortran:
	@echo "Fortran scaffold for Determinants and Invertibility"

c:
	@echo "C scaffold for Determinants and Invertibility"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
