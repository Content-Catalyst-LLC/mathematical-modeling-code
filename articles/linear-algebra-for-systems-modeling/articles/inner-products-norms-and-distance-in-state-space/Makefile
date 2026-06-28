.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,inner-products-norms-and-distance-in-state-space,Inner Products, Norms, and Distance in State Space" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Inner Products, Norms, and Distance in State Space"

python:
	@echo "Python scaffold for Inner Products, Norms, and Distance in State Space"

test:
	@echo "Python test scaffold for Inner Products, Norms, and Distance in State Space"

r:
	@echo "R scaffold for Inner Products, Norms, and Distance in State Space"

julia:
	@echo "Julia scaffold for Inner Products, Norms, and Distance in State Space"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/inner-products-norms-and-distance-in-state-space.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Inner Products, Norms, and Distance in State Space"

go:
	@echo "Go scaffold for Inner Products, Norms, and Distance in State Space"

cpp:
	@echo "C++ scaffold for Inner Products, Norms, and Distance in State Space"

fortran:
	@echo "Fortran scaffold for Inner Products, Norms, and Distance in State Space"

c:
	@echo "C scaffold for Inner Products, Norms, and Distance in State Space"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
