.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 advection_diffusion_audit.cpp -o advection_diffusion_audit; mkdir -p ../outputs/tables; ./advection_diffusion_audit > ../outputs/tables/cpp_advection_diffusion_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f advection_diffusion_audit
