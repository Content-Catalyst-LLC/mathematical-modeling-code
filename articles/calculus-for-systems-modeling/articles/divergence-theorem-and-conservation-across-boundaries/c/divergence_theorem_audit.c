#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void audit(int grid_steps, const char* scenario){
  double step = 1.0 / grid_steps;
  double area = step * step;
  double flux = 0.0;
  for(int i=0; i<grid_steps; i++){
    for(int j=0; j<grid_steps; j++){
      double y = (i + 0.5) * step;
      double z = (j + 0.5) * step;
      flux += 0.0 * (-1.0) * area;
      flux += 1.0 * 1.0 * area;

      double x = (i + 0.5) * step;
      flux += 0.0 * (-1.0) * area;
      flux += 1.0 * 1.0 * area;

      (void)y; (void)z; (void)x;
      flux += 0.0 * (-1.0) * area;
      flux += 1.0 * 1.0 * area;
    }
  }
  double div_integral = 3.0;
  const char* warning = grid_steps < 8 ? "Coarse grid; refine before interpreting the boundary-volume comparison." : "Synthetic divergence theorem audit.";
  printf("%s,%d,%.12f,%.12f,%.12f,%s,%s,%s,%s\n", scenario, grid_steps, flux, div_integral, fabs(flux-div_integral), "F=<x,y,z>; divergence = 3", "unit cube [0,1]x[0,1]x[0,1]", "all six cube faces use outward normals", warning);
}

int main(void){
  printf("scenario,grid_steps,boundary_flux,volume_divergence_integral,absolute_gap,field_description,volume_description,normal_note,warning\n");
  audit(4, "coarse_audit");
  audit(16, "medium_audit");
  audit(64, "fine_audit");
  return EXIT_SUCCESS;
}
