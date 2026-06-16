#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double rate_function(double t, double y, double k){ (void)t; return -k * y; }
static double exact_solution(double t, double y0, double k){ return y0 * exp(-k * t); }
static double rk4_step(double t, double y, double h, double k){
  double k1 = rate_function(t, y, k);
  double k2 = rate_function(t + h/2.0, y + h*k1/2.0, k);
  double k3 = rate_function(t + h/2.0, y + h*k2/2.0, k);
  double k4 = rate_function(t + h, y + h*k3, k);
  return y + (h/6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4);
}

int main(void){
  const double y0 = 100.0, k = 0.35, h = 0.5, stop_time = 20.0;
  const int steps = (int)round(stop_time / h);
  double y = y0;

  printf("step,time,solver_value,exact_value,absolute_error,solver_method,step_size,warning\n");
  for(int step=0; step<=steps; step++){
    double t = step * h;
    double exact = exact_solution(t, y0, k);
    printf("%d,%.6f,%.12f,%.12f,%.12f,fixed_step_rk4,%.6f,ODE solver outputs depend on equation initial condition method tolerances step size stiffness and diagnostics.\n",
      step, t, y, exact, fabs(y - exact), h);
    y = rk4_step(t, y, h, k);
  }
  return EXIT_SUCCESS;
}
