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
static double simulate(double y0, double k, double h, double stop_time){
  int steps = (int)round(stop_time / h);
  double y = y0;
  for(int step=0; step<steps; step++){
    y = rk4_step(step*h, y, h, k);
  }
  return y;
}
int main(void){
  const double y0 = 100.0, k = 0.35, stop_time = 20.0;
  const double exact_final = exact_solution(stop_time, y0, k);
  const double hs[4] = {1.0, 0.5, 0.25, 0.125};
  printf("step_size,steps,solver_method,final_numeric_value,final_exact_value,final_absolute_error,warning\n");
  for(int i=0; i<4; i++){
    double h = hs[i];
    double numeric = simulate(y0, k, h, stop_time);
    printf("%.6f,%d,fixed_step_rk4,%.12f,%.12f,%.12f,Convergence evidence supports numerical reliability not empirical validity.\n",
      h, (int)round(stop_time / h), numeric, exact_final, fabs(numeric - exact_final));
  }
  return EXIT_SUCCESS;
}
