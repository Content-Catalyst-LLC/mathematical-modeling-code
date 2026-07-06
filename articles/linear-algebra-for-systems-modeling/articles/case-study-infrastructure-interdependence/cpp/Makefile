.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 infrastructure_interdependence_audit.cpp -o infrastructure_interdependence_audit_cpp && ./infrastructure_interdependence_audit_cpp > ../outputs/tables/cpp_infrastructure_interdependence_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f infrastructure_interdependence_audit_cpp
