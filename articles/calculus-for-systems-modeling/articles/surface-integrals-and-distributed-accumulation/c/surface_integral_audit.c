#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double height(double x, double y){ return 0.1*x*x + 0.05*y*y; }
double scalar_field(double x, double y, double z){ (void)x; (void)y; return 1.0 + 0.2*z; }
void vector_field(double x, double y, double z, double* vx, double* vy, double* vz){ (void)z; *vx = 0.1*x; *vy = 0.1*y; *vz = 1.0; }
void normal_area_vector(double x, double y, double step, double* nx, double* ny, double* nz){
  double area = step*step;
  *nx = -0.2*x*area;
  *ny = -0.1*y*area;
  *nz = area;
}
double norm3(double x,double y,double z){ return sqrt(x*x+y*y+z*z); }
double dot3(double ax,double ay,double az,double bx,double by,double bz){ return ax*bx+ay*by+az*bz; }

void audit(double step, const char* scenario){
  int n = (int)(2.0 / step);
  int count = 0;
  double surface_area = 0.0, scalar_total = 0.0, flux_total = 0.0, flux_density_sum = 0.0, max_patch = 0.0;
  for(int i=0; i<n; i++){
    double x = -1.0 + i*step;
    for(int j=0; j<n; j++){
      double y = -1.0 + j*step;
      double z = height(x,y);
      double ax,ay,az,vx,vy,vz;
      normal_area_vector(x,y,step,&ax,&ay,&az);
      vector_field(x,y,z,&vx,&vy,&vz);
      double patch_area = norm3(ax,ay,az);
      double flux = dot3(vx,vy,vz,ax,ay,az);
      count++;
      surface_area += patch_area;
      scalar_total += scalar_field(x,y,z) * patch_area;
      flux_total += flux;
      flux_density_sum += flux / fmax(patch_area, 1e-12);
      if(patch_area > max_patch) max_patch = patch_area;
    }
  }
  const char* warning = step > 0.5 ? "Grid step is coarse; curvature and field variation may be undersampled." : "Synthetic surface-integral audit; document surface normal units and mesh.";
  printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%s\n", scenario, step, count, surface_area, scalar_total, flux_total, flux_density_sum/count, max_patch, "graph z=0.1x^2+0.05y^2", warning);
}

int main(void){
  printf("scenario,grid_step,patch_count,approximate_surface_area,scalar_surface_integral,vector_flux_integral,average_flux_density,maximum_patch_area,surface_description,warning\n");
  audit(1.0, "coarse_surface_mesh");
  audit(0.5, "medium_surface_mesh");
  audit(0.25, "fine_surface_mesh");
  return EXIT_SUCCESS;
}
