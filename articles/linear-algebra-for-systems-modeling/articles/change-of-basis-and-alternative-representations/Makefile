.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,change-of-basis-and-alternative-representations,Change of Basis and Alternative Representations" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Change of Basis and Alternative Representations"

python:
	@echo "Python scaffold for Change of Basis and Alternative Representations"

test:
	@echo "Python test scaffold for Change of Basis and Alternative Representations"

r:
	@echo "R scaffold for Change of Basis and Alternative Representations"

julia:
	@echo "Julia scaffold for Change of Basis and Alternative Representations"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/change-of-basis-and-alternative-representations.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Change of Basis and Alternative Representations"

go:
	@echo "Go scaffold for Change of Basis and Alternative Representations"

cpp:
	@echo "C++ scaffold for Change of Basis and Alternative Representations"

fortran:
	@echo "Fortran scaffold for Change of Basis and Alternative Representations"

c:
	@echo "C scaffold for Change of Basis and Alternative Representations"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
