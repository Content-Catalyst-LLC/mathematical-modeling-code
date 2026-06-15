#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <tuple>

double height(double x, double y){ return 0.1*x*x + 0.05*y*y; }
double scalar_field(double x, double y, double z){ (void)x; (void)y; return 1.0 + 0.2*z; }
std::tuple<double,double,double> vector_field(double x, double y, double z){ (void)z; return {0.1*x, 0.1*y, 1.0}; }
std::tuple<double,double,double> normal_area_vector(double x, double y, double step){
  double area = step*step;
  return {-0.2*x*area, -0.1*y*area, area};
}
double norm3(std::tuple<double,double,double> v){
  auto [x,y,z] = v;
  return std::sqrt(x*x+y*y+z*z);
}
double dot3(std::tuple<double,double,double> a, std::tuple<double,double,double> b){
  auto [ax,ay,az] = a;
  auto [bx,by,bz] = b;
  return ax*bx+ay*by+az*bz;
}

void audit(double step, const std::string& scenario){
  int n = static_cast<int>(2.0 / step);
  int count = 0;
  double surface_area = 0.0, scalar_total = 0.0, flux_total = 0.0, flux_density_sum = 0.0, max_patch = 0.0;

  for(int i=0; i<n; i++){
    double x = -1.0 + i*step;
    for(int j=0; j<n; j++){
      double y = -1.0 + j*step;
      double z = height(x,y);
      auto area_vector = normal_area_vector(x,y,step);
      auto field_vector = vector_field(x,y,z);
      double patch_area = norm3(area_vector);
      double flux = dot3(field_vector, area_vector);
      count++;
      surface_area += patch_area;
      scalar_total += scalar_field(x,y,z) * patch_area;
      flux_total += flux;
      flux_density_sum += flux / std::max(patch_area, 1e-12);
      max_patch = std::max(max_patch, patch_area);
    }
  }

  std::string warning = step > 0.5 ? "Grid step is coarse; curvature and field variation may be undersampled." : "Synthetic surface-integral audit; document surface normal units and mesh.";
  std::cout << scenario << "," << step << "," << count << "," << surface_area << "," << scalar_total << "," << flux_total << "," << flux_density_sum/count << "," << max_patch << ",graph z=0.1x^2+0.05y^2," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,grid_step,patch_count,approximate_surface_area,scalar_surface_integral,vector_flux_integral,average_flux_density,maximum_patch_area,surface_description,warning\n";
  audit(1.0, "coarse_surface_mesh");
  audit(0.5, "medium_surface_mesh");
  audit(0.25, "fine_surface_mesh");
}
