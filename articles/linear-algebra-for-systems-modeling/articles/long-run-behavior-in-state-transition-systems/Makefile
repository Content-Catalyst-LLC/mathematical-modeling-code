.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,long-run-behavior-in-state-transition-systems,Long-Run Behavior in State Transition Systems" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Long-Run Behavior in State Transition Systems"

python:
	@echo "Python scaffold for Long-Run Behavior in State Transition Systems"

test:
	@echo "Python test scaffold for Long-Run Behavior in State Transition Systems"

r:
	@echo "R scaffold for Long-Run Behavior in State Transition Systems"

julia:
	@echo "Julia scaffold for Long-Run Behavior in State Transition Systems"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/long-run-behavior-in-state-transition-systems.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Long-Run Behavior in State Transition Systems"

go:
	@echo "Go scaffold for Long-Run Behavior in State Transition Systems"

cpp:
	@echo "C++ scaffold for Long-Run Behavior in State Transition Systems"

fortran:
	@echo "Fortran scaffold for Long-Run Behavior in State Transition Systems"

c:
	@echo "C scaffold for Long-Run Behavior in State Transition Systems"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
