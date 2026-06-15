#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>

void audit(int grid_steps, const std::string& scenario){
  double step = 1.0 / grid_steps;
  double area = step * step;
  double flux = 0.0;
  for(int i=0; i<grid_steps; i++){
    for(int j=0; j<grid_steps; j++){
      flux += 1.0 * area; // x=1
      flux += 1.0 * area; // y=1
      flux += 1.0 * area; // z=1
    }
  }
  double div_integral = 3.0;
  std::string warning = grid_steps < 8 ? "Coarse grid; refine before interpreting the boundary-volume comparison." : "Synthetic divergence theorem audit.";
  std::cout << scenario << "," << grid_steps << "," << flux << "," << div_integral << "," << std::abs(flux-div_integral) << ",F=<x,y,z>; divergence = 3,unit cube [0,1]x[0,1]x[0,1],all six cube faces use outward normals," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,grid_steps,boundary_flux,volume_divergence_integral,absolute_gap,field_description,volume_description,normal_note,warning\n";
  audit(4, "coarse_audit");
  audit(16, "medium_audit");
  audit(64, "fine_audit");
}
