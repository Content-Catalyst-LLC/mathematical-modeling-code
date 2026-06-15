#include <algorithm>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

int main(){
  const int grid_points = 61;
  const int steps = 120;
  const double diffusivity = 0.08, velocity = 0.4, dx = 1.0, dt = 0.2;
  const double d_ratio = diffusivity * dt / (dx * dx);
  const double t_ratio = velocity * dt / dx;

  std::vector<double> field(grid_points, 0.0);
  field[grid_points / 2] = 1.0;

  std::cout << std::fixed << std::setprecision(6);
  std::cout << "step,time,center_value,total_mass,max_value,min_value,diffusion_ratio,transport_ratio,warning\n";

  for(int step=0; step<=steps; step++){
    double total = std::accumulate(field.begin(), field.end(), 0.0) * dx;
    double maxv = *std::max_element(field.begin(), field.end());
    double minv = *std::min_element(field.begin(), field.end());
    std::cout << step << "," << step*dt << "," << field[grid_points/2] << "," << total << "," << maxv << "," << minv << "," << d_ratio << "," << t_ratio << ",Spatial dynamics depend on field meaning boundary conditions grid spacing time step and numerical stability.\n";

    std::vector<double> updated = field;
    for(int i=1; i<grid_points-1; i++){
      double diffusion_part = d_ratio * (field[i+1] - 2.0*field[i] + field[i-1]);
      double transport_part = -t_ratio * (field[i] - field[i-1]);
      updated[i] = field[i] + diffusion_part + transport_part;
    }
    updated[0] = 0.0;
    updated[grid_points-1] = 0.0;
    field = updated;
  }
}
