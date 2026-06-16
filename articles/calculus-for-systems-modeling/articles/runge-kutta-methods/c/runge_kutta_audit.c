#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double rate_function(double t, double y, double k){ (void)t; return -k * y; }
static double exact_solution(double t, double y0, double k){ return y0 * exp(-k * t); }
static double euler_step(double t, double y, double h, double k){ return y + h * rate_function(t, y, k); }
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
  double y_euler = y0;
  double y_rk4 = y0;

  printf("step,time,euler_value,rk4_value,exact_value,euler_absolute_error,rk4_absolute_error,step_size,warning\n");
  for(int step=0; step<=steps; step++){
    double t = step * h;
    double exact = exact_solution(t, y0, k);
    printf("%d,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.6f,Runge-Kutta estimates depend on rate function step size smoothness stiffness and benchmark comparison.\n",
      step, t, y_euler, y_rk4, exact, fabs(y_euler - exact), fabs(y_rk4 - exact), h);
    y_euler = euler_step(t, y_euler, h, k);
    y_rk4 = rk4_step(t, y_rk4, h, k);
  }
  return EXIT_SUCCESS;
}
