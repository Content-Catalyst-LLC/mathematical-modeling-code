#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>

double scalar_field(double x, double y){ return 20.0 + 2.0*std::sin(x) + 0.5*y*y; }
std::pair<double,double> vector_field(double x, double y){ return {-y, x}; }
double vector_magnitude(double vx, double vy){ return std::sqrt(vx*vx + vy*vy); }

void audit(double step, const std::string& scenario){
  int n = static_cast<int>(6.0 / step);
  int count = 0;
  double scalar_sum = 0.0, scalar_min = 1e99, scalar_max = -1e99;
  double mag_sum = 0.0, mag_max = 0.0;

  for(int i=0; i<=n; i++){
    double x = -3.0 + i*step;
    for(int j=0; j<=n; j++){
      double y = -3.0 + j*step;
      double s = scalar_field(x, y);
      auto [vx, vy] = vector_field(x, y);
      double mag = vector_magnitude(vx, vy);
      count++;
      scalar_sum += s;
      scalar_min = std::min(scalar_min, s);
      scalar_max = std::max(scalar_max, s);
      mag_sum += mag;
      mag_max = std::max(mag_max, mag);
    }
  }
  std::string warning = step > 0.75 ? "Grid resolution is coarse; field structure may be undersampled." : "Synthetic field audit; document domain units and interpolation assumptions.";
  std::cout << scenario << "," << step << "," << count << "," << scalar_sum/count << "," << scalar_min << "," << scalar_max << "," << mag_sum/count << "," << mag_max << ",square domain [-3,3] x [-3,3]," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,grid_step,point_count,scalar_average,scalar_minimum,scalar_maximum,vector_magnitude_average,vector_magnitude_maximum,domain_description,warning\n";
  audit(1.0, "coarse_grid");
  audit(0.5, "medium_grid");
  audit(0.25, "fine_grid");
}
