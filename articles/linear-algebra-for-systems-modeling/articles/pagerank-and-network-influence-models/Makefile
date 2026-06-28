.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,pagerank-and-network-influence-models,PageRank and Network Influence Models" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for PageRank and Network Influence Models"

python:
	@echo "Python scaffold for PageRank and Network Influence Models"

test:
	@echo "Python test scaffold for PageRank and Network Influence Models"

r:
	@echo "R scaffold for PageRank and Network Influence Models"

julia:
	@echo "Julia scaffold for PageRank and Network Influence Models"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/pagerank-and-network-influence-models.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for PageRank and Network Influence Models"

go:
	@echo "Go scaffold for PageRank and Network Influence Models"

cpp:
	@echo "C++ scaffold for PageRank and Network Influence Models"

fortran:
	@echo "Fortran scaffold for PageRank and Network Influence Models"

c:
	@echo "C scaffold for PageRank and Network Influence Models"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
