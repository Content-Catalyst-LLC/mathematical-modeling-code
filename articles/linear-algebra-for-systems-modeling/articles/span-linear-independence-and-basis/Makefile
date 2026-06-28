.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,span-linear-independence-and-basis,Span, Linear Independence, and Basis" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Span, Linear Independence, and Basis"

python:
	@echo "Python scaffold for Span, Linear Independence, and Basis"

test:
	@echo "Python test scaffold for Span, Linear Independence, and Basis"

r:
	@echo "R scaffold for Span, Linear Independence, and Basis"

julia:
	@echo "Julia scaffold for Span, Linear Independence, and Basis"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/span-linear-independence-and-basis.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Span, Linear Independence, and Basis"

go:
	@echo "Go scaffold for Span, Linear Independence, and Basis"

cpp:
	@echo "C++ scaffold for Span, Linear Independence, and Basis"

fortran:
	@echo "Fortran scaffold for Span, Linear Independence, and Basis"

c:
	@echo "C scaffold for Span, Linear Independence, and Basis"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
