.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,case-study-state-transition-and-markov-dynamics,Case Study: State Transition and Markov Dynamics" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Case Study: State Transition and Markov Dynamics"

python:
	@echo "Python scaffold for Case Study: State Transition and Markov Dynamics"

test:
	@echo "Python test scaffold for Case Study: State Transition and Markov Dynamics"

r:
	@echo "R scaffold for Case Study: State Transition and Markov Dynamics"

julia:
	@echo "Julia scaffold for Case Study: State Transition and Markov Dynamics"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/case-study-state-transition-and-markov-dynamics.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Case Study: State Transition and Markov Dynamics"

go:
	@echo "Go scaffold for Case Study: State Transition and Markov Dynamics"

cpp:
	@echo "C++ scaffold for Case Study: State Transition and Markov Dynamics"

fortran:
	@echo "Fortran scaffold for Case Study: State Transition and Markov Dynamics"

c:
	@echo "C scaffold for Case Study: State Transition and Markov Dynamics"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
