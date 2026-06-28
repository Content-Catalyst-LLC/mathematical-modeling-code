.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,case-study-infrastructure-interdependence,Case Study: Infrastructure Interdependence" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Case Study: Infrastructure Interdependence"

python:
	@echo "Python scaffold for Case Study: Infrastructure Interdependence"

test:
	@echo "Python test scaffold for Case Study: Infrastructure Interdependence"

r:
	@echo "R scaffold for Case Study: Infrastructure Interdependence"

julia:
	@echo "Julia scaffold for Case Study: Infrastructure Interdependence"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/case-study-infrastructure-interdependence.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Case Study: Infrastructure Interdependence"

go:
	@echo "Go scaffold for Case Study: Infrastructure Interdependence"

cpp:
	@echo "C++ scaffold for Case Study: Infrastructure Interdependence"

fortran:
	@echo "Fortran scaffold for Case Study: Infrastructure Interdependence"

c:
	@echo "C scaffold for Case Study: Infrastructure Interdependence"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
