.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 pde_diffusion_grid_audit.cpp -o pde_diffusion_grid_audit; mkdir -p ../outputs/tables; ./pde_diffusion_grid_audit > ../outputs/tables/cpp_pde_diffusion_grid_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f pde_diffusion_grid_audit
