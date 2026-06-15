#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double factorial_int(int n){
  double result = 1.0;
  for(int i=2; i<=n; i++){ result *= (double)i; }
  return result;
}

double taylor_exp(double x, int order){
  double total = 0.0;
  for(int n=0; n<=order; n++){ total += pow(x, n) / factorial_int(n); }
  return total;
}

int main(void){
  double xs[] = {0.5, 1.0, 3.0};
  int orders[] = {2, 10, 10};
  printf("method,function_name,center,x_value,order,approximation,reference_value,absolute_error,relative_error,warning\n");
  for(int i=0; i<3; i++){
    double x = xs[i];
    int order = orders[i];
    double approx = taylor_exp(x, order);
    double reference = exp(x);
    double abs_err = fabs(reference-approx);
    double rel_err = abs_err / fabs(reference);
    const char* warning = fabs(x) <= 2.0 ? "" : "Evaluation is far from the expansion center; review local validity.";
    printf("Maclaurin truncation,exp(x),0.0,%.6f,%d,%.12f,%.12f,%.12f,%.12f,%s\n", x, order, approx, reference, abs_err, rel_err, warning);
  }
  return EXIT_SUCCESS;
}
