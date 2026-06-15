#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double geometric_sum(double a, double r, int n){
  double total = 0.0;
  for(int i=0;i<n;i++){ total += a * pow(r, i); }
  return total;
}

double p_series_sum(double p, int n){
  double total = 0.0;
  for(int i=1;i<=n;i++){ total += 1.0 / pow((double)i, p); }
  return total;
}

int main(void){
  double geo = geometric_sum(10.0, 0.6, 25);
  double geo_ref = 10.0 / (1.0 - 0.6);
  double p125 = p_series_sum(1.25, 10000);
  double p075 = p_series_sum(0.75, 10000);

  printf("series_name,test_used,n_terms,partial_sum,last_term,test_result,estimated_error\n");
  printf("geometric_r_0.6,geometric-series test,25,%.12f,%.12f,converges by geometric-series test,%.12f\n",geo,10.0*pow(0.6,24),geo_ref-geo);
  printf("p_series_1.25,p-series test,10000,%.12f,%.12f,converges,\n",p125,1.0/pow(10000.0,1.25));
  printf("p_series_0.75,p-series test,10000,%.12f,%.12f,diverges,\n",p075,1.0/pow(10000.0,0.75));
  return EXIT_SUCCESS;
}
