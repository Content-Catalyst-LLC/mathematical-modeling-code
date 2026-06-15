#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double geometric_power_series(double x, int n_terms){
  double total = 0.0;
  for(int n=0; n<n_terms; n++){ total += pow(x, n); }
  return total;
}

int main(void){
  double xs[] = {0.25, 0.75, 1.25};
  int ns[] = {5, 20, 10};
  printf("function_name,center,x_value,n_terms,partial_sum,reference_value,absolute_error,convergence_status,warning\n");
  for(int i=0; i<3; i++){
    double x = xs[i];
    int n_terms = ns[i];
    double partial = geometric_power_series(x, n_terms);
    int converges = fabs(x) < 1.0;
    if(converges){
      double reference = 1.0 / (1.0 - x);
      printf("1/(1-x),0.0,%.6f,%d,%.12f,%.12f,%.12f,inside radius of convergence,\n",
             x, n_terms, partial, reference, fabs(reference - partial));
    } else {
      printf("1/(1-x),0.0,%.6f,%d,%.12f,,,outside radius of convergence,Power series does not converge for this x value.\n",
             x, n_terms, partial);
    }
  }
  return EXIT_SUCCESS;
}
