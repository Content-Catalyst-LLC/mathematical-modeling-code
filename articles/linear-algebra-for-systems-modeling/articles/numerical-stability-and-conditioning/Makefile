.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,numerical-stability-and-conditioning,Numerical Stability and Conditioning" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Numerical Stability and Conditioning"

python:
	@echo "Python scaffold for Numerical Stability and Conditioning"

test:
	@echo "Python test scaffold for Numerical Stability and Conditioning"

r:
	@echo "R scaffold for Numerical Stability and Conditioning"

julia:
	@echo "Julia scaffold for Numerical Stability and Conditioning"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/numerical-stability-and-conditioning.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Numerical Stability and Conditioning"

go:
	@echo "Go scaffold for Numerical Stability and Conditioning"

cpp:
	@echo "C++ scaffold for Numerical Stability and Conditioning"

fortran:
	@echo "Fortran scaffold for Numerical Stability and Conditioning"

c:
	@echo "C scaffold for Numerical Stability and Conditioning"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
