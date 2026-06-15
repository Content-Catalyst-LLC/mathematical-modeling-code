#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double exposure_field(double x, double y){ return 10.0 + 2.0*x + 0.5*y*y; }
double population_density(double x, double y){ return 100.0 + 10.0*y + 5.0*sin(x); }
int in_region(double x, double y){ return x*x + y*y <= 9.0; }

void compute(double step, const char* scenario){
  int n = (int)(6.0 / step);
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
  const char* warning = step > 0.5 ? "Grid resolution is coarse; spatial accumulation may smooth local variation." : "Synthetic grid audit; region mask cell area and units should be documented.";
  printf("%s,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s\n",
    scenario, cells, cell_area, total_area, total_density,
    total_density/total_area, population_burden, total_population,
    population_burden/total_population, warning);
}

int main(void){
  printf("scenario,cells_in_region,cell_area,total_area,total_density_accumulation,area_weighted_average,population_weighted_burden,population_total,population_weighted_average_exposure,warning\n");
  compute(1.0, "coarse_grid");
  compute(0.5, "medium_grid");
  compute(0.25, "fine_grid");
  return EXIT_SUCCESS;
}
