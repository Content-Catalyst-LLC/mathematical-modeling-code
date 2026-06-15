#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double exposure_field(double x, double y){ return 10.0 + 2.0*x + 0.5*y*y; }
double population_density(double x, double y){ return 100.0 + 10.0*y + 5.0*std::sin(x); }
bool in_region(double x, double y){ return x*x + y*y <= 9.0; }

void compute(double step, const std::string& scenario){
  int n = static_cast<int>(6.0 / step);
  double cell_area = step * step;
  int cells = 0;
  double total_density = 0.0, total_population = 0.0, population_burden = 0.0;
  for(int i=0; i<=n; i++){
    double x = -3.0 + i*step;
    for(int j=0; j<=n; j++){
      double y = -3.0 + j*step;
      if(in_region(x,y)){
        double exposure = exposure_field(x,y);
        double population = population_density(x,y);
        cells++;
        total_density += exposure * cell_area;
        total_population += population * cell_area;
        population_burden += exposure * population * cell_area;
      }
    }
  }
  double total_area = cells * cell_area;
  std::string warning = step > 0.5 ? "Grid resolution is coarse; spatial accumulation may smooth local variation." : "Synthetic grid audit; region mask cell area and units should be documented.";
  std::cout << scenario << "," << cells << "," << cell_area << "," << total_area << "," << total_density << "," << total_density/total_area << "," << population_burden << "," << total_population << "," << population_burden/total_population << "," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,cells_in_region,cell_area,total_area,total_density_accumulation,area_weighted_average,population_weighted_burden,population_total,population_weighted_average_exposure,warning\n";
  compute(1.0, "coarse_grid");
  compute(0.5, "medium_grid");
  compute(0.25, "fine_grid");
}
