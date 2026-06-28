.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 linear_transformation_behavior_audit.cpp -o linear_transformation_behavior_audit_cpp && ./linear_transformation_behavior_audit_cpp > ../outputs/tables/cpp_linear_transformation_behavior_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f linear_transformation_behavior_audit_cpp
