.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 stability_conditioning_audit.cpp -o stability_conditioning_audit_cpp && ./stability_conditioning_audit_cpp > ../outputs/tables/cpp_stability_conditioning_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f stability_conditioning_audit_cpp
