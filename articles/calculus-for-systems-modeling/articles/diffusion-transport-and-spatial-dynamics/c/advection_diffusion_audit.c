#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void){
  const int grid_points = 61;
  const int steps = 120;
  const double diffusivity = 0.08, velocity = 0.4, dx = 1.0, dt = 0.2;
  const double d_ratio = diffusivity * dt / (dx * dx);
  const double t_ratio = velocity * dt / dx;
  double field[grid_points];
  double updated[grid_points];

  for(int i=0; i<grid_points; i++){ field[i] = 0.0; }
  field[grid_points/2] = 1.0;

  printf("step,time,center_value,total_mass,max_value,min_value,diffusion_ratio,transport_ratio,warning\n");
  for(int step=0; step<=steps; step++){
    double total = 0.0, maxv = field[0], minv = field[0];
    for(int i=0; i<grid_points; i++){
      total += field[i] * dx;
      if(field[i] > maxv) maxv = field[i];
      if(field[i] < minv) minv = field[i];
    }
    printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Spatial dynamics depend on field meaning boundary conditions grid spacing time step and numerical stability.\n",
      step, step*dt, field[grid_points/2], total, maxv, minv, d_ratio, t_ratio);

    for(int i=0; i<grid_points; i++){ updated[i] = field[i]; }
    for(int i=1; i<grid_points-1; i++){
      double diffusion_part = d_ratio * (field[i+1] - 2.0*field[i] + field[i-1]);
      double transport_part = -t_ratio * (field[i] - field[i-1]);
      updated[i] = field[i] + diffusion_part + transport_part;
    }
    updated[0] = 0.0;
    updated[grid_points-1] = 0.0;
    for(int i=0; i<grid_points; i++){ field[i] = updated[i]; }
  }
  return EXIT_SUCCESS;
}
