.PHONY: all smoke python test r julia sql haskell rust go cpp fortran c advanced clean

all: smoke

smoke:
	@mkdir -p outputs/json outputs/logs outputs/tables
	@echo "planned,markov-chains-and-transition-matrices,Markov Chains and Transition Matrices" > outputs/tables/article_status.csv
	@echo "Smoke scaffold complete for Markov Chains and Transition Matrices"

python:
	@echo "Python scaffold for Markov Chains and Transition Matrices"

test:
	@echo "Python test scaffold for Markov Chains and Transition Matrices"

r:
	@echo "R scaffold for Markov Chains and Transition Matrices"

julia:
	@echo "Julia scaffold for Markov Chains and Transition Matrices"

sql:
	@mkdir -p outputs/tables
	@sqlite3 outputs/tables/markov-chains-and-transition-matrices.sqlite < sql/schema.sql || true

haskell:
	$(MAKE) -C haskell run || true

rust:
	@echo "Rust scaffold for Markov Chains and Transition Matrices"

go:
	@echo "Go scaffold for Markov Chains and Transition Matrices"

cpp:
	@echo "C++ scaffold for Markov Chains and Transition Matrices"

fortran:
	@echo "Fortran scaffold for Markov Chains and Transition Matrices"

c:
	@echo "C scaffold for Markov Chains and Transition Matrices"

advanced:
	$(MAKE) -C advanced smoke

clean:
	rm -f outputs/tables/*.csv outputs/tables/*.txt outputs/tables/*.sqlite
	rm -f outputs/json/*.json outputs/logs/*.log
