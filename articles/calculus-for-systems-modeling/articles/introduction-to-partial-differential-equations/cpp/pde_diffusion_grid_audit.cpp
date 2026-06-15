#include <algorithm>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

int main(){
  const int grid_points = 51;
  const int steps = 100;
  const double diffusivity = 0.1, dx = 1.0, dt = 0.25;
  const double ratio = diffusivity * dt / (dx * dx);

  std::vector<double> field(grid_points, 0.0);
  field[grid_points / 2] = 1.0;

  std::cout << std::fixed << std::setprecision(6);
  std::cout << "step,time,center_value,total_mass,max_value,min_value,stability_ratio,warning\n";

  for(int step=0; step<=steps; step++){
    double total = std::accumulate(field.begin(), field.end(), 0.0) * dx;
    double maxv = *std::max_element(field.begin(), field.end());
    double minv = *std::min_element(field.begin(), field.end());
    std::cout << step << "," << step*dt << "," << field[grid_points/2] << "," << total << "," << maxv << "," << minv << "," << ratio << ",Explicit diffusion schemes require stability checks boundary and grid assumptions shape results.\n";

    std::vector<double> updated = field;
    for(int i=1; i<grid_points-1; i++){
      updated[i] = field[i] + ratio*(field[i+1] - 2*field[i] + field[i-1]);
    }
    updated[0] = 0.0;
    updated[grid_points-1] = 0.0;
    field = updated;
  }
}
