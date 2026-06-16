#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double signal_function(double x){ return sin(x) + 0.1 * x * x; }
static double true_derivative(double x){ return cos(x) + 0.2 * x; }

int main(void){
  const double start = 0.0, stop = 10.0, h = 0.1;
  const int n = (int)round((stop - start) / h);
  double xs[n + 1];
  double values[n + 1];

  for(int i=0; i<=n; i++){
    xs[i] = start + i * h;
    values[i] = signal_function(xs[i]);
  }

  printf("index,x,value,true_derivative,forward_difference,backward_difference,central_difference,central_absolute_error,step_size,warning\n");
  for(int i=0; i<=n; i++){
    double forward = NAN, backward = NAN, central = NAN, err = NAN;
    if(i < n){ forward = (values[i+1] - values[i]) / h; }
    if(i > 0){ backward = (values[i] - values[i-1]) / h; }
    if(i > 0 && i < n){
      central = (values[i+1] - values[i-1]) / (2.0*h);
      err = fabs(central - true_derivative(xs[i]));
    }
    printf("%d,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.6f,Numerical derivatives depend on step size formula choice boundary handling smoothness and noise.\n",
      i, xs[i], values[i], true_derivative(xs[i]), forward, backward, central, err, h);
  }
  return EXIT_SUCCESS;
}
