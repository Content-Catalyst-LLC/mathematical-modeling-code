#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double geometric_sum(double a, double r, int n){
  double total = 0.0;
  for(int i=0;i<n;i++){ total += a * pow(r, i); }
  return total;
}

double harmonic_sum(int n){
  double total = 0.0;
  for(int i=1;i<=n;i++){ total += 1.0 / i; }
  return total;
}

int main(void){
  double geo = geometric_sum(10.0, 0.6, 25);
  double geo_ref = 10.0 / (1.0 - 0.6);
  double harm = harmonic_sum(10000);
  printf("series_name,n_terms,last_term,partial_sum,reference_value,estimated_error,convergence_classification\n");
  printf("geometric_r_0.6,25,%.12f,%.12f,%.12f,%.12f,convergent geometric series\n",10.0*pow(0.6,24),geo,geo_ref,geo_ref-geo);
  printf("harmonic,10000,%.12f,%.12f,,,divergent despite terms approaching zero\n",1.0/10000.0,harm);
  return EXIT_SUCCESS;
}
