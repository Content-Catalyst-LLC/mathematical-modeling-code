.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 reproducible_calculus_workflows.cpp -o reproducible_calculus_workflows; mkdir -p ../outputs/tables; ./reproducible_calculus_workflows > ../outputs/tables/cpp_workflow_artifacts.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f reproducible_calculus_workflows
