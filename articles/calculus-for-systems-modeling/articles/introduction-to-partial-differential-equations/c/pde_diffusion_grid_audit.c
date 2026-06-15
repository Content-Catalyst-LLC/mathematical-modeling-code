#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void){
  const int grid_points = 51;
  const int steps = 100;
  const double diffusivity = 0.1, dx = 1.0, dt = 0.25;
  const double ratio = diffusivity * dt / (dx * dx);
  double field[grid_points];
  double updated[grid_points];

  for(int i=0; i<grid_points; i++){ field[i] = 0.0; }
  field[grid_points/2] = 1.0;

  printf("step,time,center_value,total_mass,max_value,min_value,stability_ratio,warning\n");
  for(int step=0; step<=steps; step++){
    double total = 0.0, maxv = field[0], minv = field[0];
    for(int i=0; i<grid_points; i++){
      total += field[i] * dx;
      if(field[i] > maxv) maxv = field[i];
      if(field[i] < minv) minv = field[i];
    }
    printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Explicit diffusion schemes require stability checks boundary and grid assumptions shape results.\n",
      step, step*dt, field[grid_points/2], total, maxv, minv, ratio);

    for(int i=0; i<grid_points; i++){ updated[i] = field[i]; }
    for(int i=1; i<grid_points-1; i++){ updated[i] = field[i] + ratio*(field[i+1] - 2*field[i] + field[i-1]); }
    updated[0] = 0.0;
    updated[grid_points-1] = 0.0;
    for(int i=0; i<grid_points; i++){ field[i] = updated[i]; }
  }
  return EXIT_SUCCESS;
}
