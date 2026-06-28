.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,scaling-normalization-and-comparative-structure,Scaling, Normalization, and Comparative Structure" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Scaling, Normalization, and Comparative Structure"

python:
	@echo "Python scaffold for Scaling, Normalization, and Comparative Structure"

test:
	@echo "Python test scaffold for Scaling, Normalization, and Comparative Structure"

r:
	@echo "R scaffold for Scaling, Normalization, and Comparative Structure"

julia:
	@echo "Julia scaffold for Scaling, Normalization, and Comparative Structure"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/scaling-normalization-and-comparative-structure.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Scaling, Normalization, and Comparative Structure"

go:
	@echo "Go scaffold for Scaling, Normalization, and Comparative Structure"

cpp:
	@echo "C++ scaffold for Scaling, Normalization, and Comparative Structure"

fortran:
	@echo "Fortran scaffold for Scaling, Normalization, and Comparative Structure"

c:
	@echo "C scaffold for Scaling, Normalization, and Comparative Structure"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
