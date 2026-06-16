#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double exact_solution(double t, double y0, double lambda){ return y0 * exp(lambda * t); }
static double explicit_value(double y0, double lambda, double h, double stop_time){
  int steps = (int)round(stop_time / h);
  double amp = 1.0 + h * lambda;
  double y = y0;
  for(int i=0; i<steps; i++){ y *= amp; }
  return y;
}
static double implicit_value(double y0, double lambda, double h, double stop_time){
  int steps = (int)round(stop_time / h);
  double amp = 1.0 / (1.0 - h * lambda);
  double y = y0;
  for(int i=0; i<steps; i++){ y *= amp; }
  return y;
}
int main(void){
  const double y0 = 1.0, lambda = -50.0, stop_time = 1.0;
  const double exact_final = exact_solution(stop_time, y0, lambda);
  const double hs[4] = {0.1, 0.05, 0.025, 0.01};
  printf("step_size,eigenvalue,method,amplification_factor,stability_status,final_value,exact_final_value,absolute_error,warning\n");
  for(int i=0; i<4; i++){
    double h = hs[i];
    double ev = explicit_value(y0, lambda, h, stop_time);
    double eamp = fabs(1.0 + h * lambda);
    double iv = implicit_value(y0, lambda, h, stop_time);
    double iamp = fabs(1.0 / (1.0 - h * lambda));
    printf("%.6f,%.6f,explicit_euler,%.12f,%s,%.12f,%.12f,%.12f,Explicit methods may require very small steps on stiff systems.\n", h, lambda, eamp, eamp <= 1.0 ? "stable_for_test_problem" : "unstable_for_test_problem", ev, exact_final, fabs(ev - exact_final));
    printf("%.6f,%.6f,implicit_euler,%.12f,%s,%.12f,%.12f,%.12f,Implicit stability does not remove accuracy review.\n", h, lambda, iamp, iamp <= 1.0 ? "stable_for_test_problem" : "unstable_for_test_problem", iv, exact_final, fabs(iv - exact_final));
  }
  return EXIT_SUCCESS;
}
