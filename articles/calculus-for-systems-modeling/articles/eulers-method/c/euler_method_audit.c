#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double exact_solution(double t, double y0, double k){ return y0 * exp(-k * t); }

int main(void){
  const double y0 = 100.0, k = 0.35, h = 0.1, stop_time = 20.0;
  const int steps = (int)round(stop_time / h);
  double y = y0;
  double multiplier = 1.0 - h * k;
  const char *status = fabs(multiplier) <= 1.0 ? "stable_for_simple_decay" : "unstable_risk";

  printf("step,time,euler_value,exact_value,absolute_error,step_size,stability_multiplier,stability_status,warning\n");
  for(int step=0; step<=steps; step++){
    double t = step * h;
    double exact = exact_solution(t, y0, k);
    printf("%d,%.6f,%.12f,%.12f,%.12f,%.6f,%.12f,%s,Euler estimates depend on time step rate function initial condition stability and accumulated error.\n",
      step, t, y, exact, fabs(y - exact), h, multiplier, status);
    y = y + h * (-k * y);
  }
  return EXIT_SUCCESS;
}
