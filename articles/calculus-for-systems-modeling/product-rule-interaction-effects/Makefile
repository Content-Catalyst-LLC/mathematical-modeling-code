.PHONY: smoke python r julia c cpp fortran go rust

smoke: python
	@python3 tests/smoke_check.py

python:
	@PYTHONPATH=python python3 -m product_rule_interaction_effects.cli --base-dir .

r:
	@Rscript r/product_rule_decomposition.R

julia:
	@julia julia/product_rule_decomposition.jl

c:
	@cc -std=c11 -Wall -Wextra c/src/product_rule.c -o outputs/product_rule_c_demo
	@./outputs/product_rule_c_demo

cpp:
	@c++ -std=c++20 -Wall -Wextra cpp/src/product_rule.cpp -o outputs/product_rule_cpp_demo
	@./outputs/product_rule_cpp_demo

fortran:
	@gfortran fortran/src/product_rule.f90 -o outputs/product_rule_fortran_demo
	@./outputs/product_rule_fortran_demo

go:
	@cd go && go run ./cmd/product_rule

rust:
	@cd rust && cargo run
