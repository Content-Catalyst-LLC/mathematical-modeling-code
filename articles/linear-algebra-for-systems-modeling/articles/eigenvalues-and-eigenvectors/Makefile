.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,eigenvalues-and-eigenvectors,Eigenvalues and Eigenvectors" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Eigenvalues and Eigenvectors"

python:
	@echo "Python scaffold for Eigenvalues and Eigenvectors"

test:
	@echo "Python test scaffold for Eigenvalues and Eigenvectors"

r:
	@echo "R scaffold for Eigenvalues and Eigenvectors"

julia:
	@echo "Julia scaffold for Eigenvalues and Eigenvectors"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/eigenvalues-and-eigenvectors.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Eigenvalues and Eigenvectors"

go:
	@echo "Go scaffold for Eigenvalues and Eigenvectors"

cpp:
	@echo "C++ scaffold for Eigenvalues and Eigenvectors"

fortran:
	@echo "Fortran scaffold for Eigenvalues and Eigenvectors"

c:
	@echo "C scaffold for Eigenvalues and Eigenvectors"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
