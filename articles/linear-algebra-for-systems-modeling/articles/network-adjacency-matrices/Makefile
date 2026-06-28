.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,network-adjacency-matrices,Network Adjacency Matrices" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Network Adjacency Matrices"

python:
	@echo "Python scaffold for Network Adjacency Matrices"

test:
	@echo "Python test scaffold for Network Adjacency Matrices"

r:
	@echo "R scaffold for Network Adjacency Matrices"

julia:
	@echo "Julia scaffold for Network Adjacency Matrices"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/network-adjacency-matrices.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Network Adjacency Matrices"

go:
	@echo "Go scaffold for Network Adjacency Matrices"

cpp:
	@echo "C++ scaffold for Network Adjacency Matrices"

fortran:
	@echo "Fortran scaffold for Network Adjacency Matrices"

c:
	@echo "C scaffold for Network Adjacency Matrices"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
