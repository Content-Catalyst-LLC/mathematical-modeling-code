.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,infrastructure-network-models,Infrastructure Network Models" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Infrastructure Network Models"

python:
	@echo "Python scaffold for Infrastructure Network Models"

test:
	@echo "Python test scaffold for Infrastructure Network Models"

r:
	@echo "R scaffold for Infrastructure Network Models"

julia:
	@echo "Julia scaffold for Infrastructure Network Models"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/infrastructure-network-models.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Infrastructure Network Models"

go:
	@echo "Go scaffold for Infrastructure Network Models"

cpp:
	@echo "C++ scaffold for Infrastructure Network Models"

fortran:
	@echo "Fortran scaffold for Infrastructure Network Models"

c:
	@echo "C scaffold for Infrastructure Network Models"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
