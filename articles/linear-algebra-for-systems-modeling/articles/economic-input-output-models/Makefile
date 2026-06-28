.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,economic-input-output-models,Economic Input-Output Models" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Economic Input-Output Models"

python:
	@echo "Python scaffold for Economic Input-Output Models"

test:
	@echo "Python test scaffold for Economic Input-Output Models"

r:
	@echo "R scaffold for Economic Input-Output Models"

julia:
	@echo "Julia scaffold for Economic Input-Output Models"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/economic-input-output-models.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Economic Input-Output Models"

go:
	@echo "Go scaffold for Economic Input-Output Models"

cpp:
	@echo "C++ scaffold for Economic Input-Output Models"

fortran:
	@echo "Fortran scaffold for Economic Input-Output Models"

c:
	@echo "C scaffold for Economic Input-Output Models"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
