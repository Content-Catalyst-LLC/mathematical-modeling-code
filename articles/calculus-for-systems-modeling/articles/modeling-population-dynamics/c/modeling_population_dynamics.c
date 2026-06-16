#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double exponential_population(double n0, double r, double t) {
  return n0 * exp(r * t);
}

double logistic_population(double n0, double r, double k, double t) {
  return k / (1.0 + ((k - n0) / n0) * exp(-r * t));
}

int main(void){
  double n0 = 100.0, r = 0.08, k = 1000.0;
  printf("time,exponential,logistic\n");
  for (int t = 0; t <= 40; ++t) {
    printf("%d,%.6f,%.6f\n", t, exponential_population(n0, r, (double)t), logistic_population(n0, r, k, (double)t));
  }
  return EXIT_SUCCESS;
}
