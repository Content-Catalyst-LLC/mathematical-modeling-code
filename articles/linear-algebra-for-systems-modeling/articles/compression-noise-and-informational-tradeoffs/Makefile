.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,compression-noise-and-informational-tradeoffs,Compression, Noise, and Informational Tradeoffs" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Compression, Noise, and Informational Tradeoffs"

python:
	@echo "Python scaffold for Compression, Noise, and Informational Tradeoffs"

test:
	@echo "Python test scaffold for Compression, Noise, and Informational Tradeoffs"

r:
	@echo "R scaffold for Compression, Noise, and Informational Tradeoffs"

julia:
	@echo "Julia scaffold for Compression, Noise, and Informational Tradeoffs"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/compression-noise-and-informational-tradeoffs.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Compression, Noise, and Informational Tradeoffs"

go:
	@echo "Go scaffold for Compression, Noise, and Informational Tradeoffs"

cpp:
	@echo "C++ scaffold for Compression, Noise, and Informational Tradeoffs"

fortran:
	@echo "Fortran scaffold for Compression, Noise, and Informational Tradeoffs"

c:
	@echo "C scaffold for Compression, Noise, and Informational Tradeoffs"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
