#include <cmath>
#include <iomanip>
#include <iostream>

double geometric_sum(double a, double r, int n){
  double total = 0.0;
  for(int i=0;i<n;i++){ total += a * std::pow(r, i); }
  return total;
}

double harmonic_sum(int n){
  double total = 0.0;
  for(int i=1;i<=n;i++){ total += 1.0 / i; }
  return total;
}

int main(){
  double geo = geometric_sum(10.0, 0.6, 25);
  double geo_ref = 10.0 / (1.0 - 0.6);
  double harm = harmonic_sum(10000);
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"series_name,n_terms,last_term,partial_sum,reference_value,estimated_error,convergence_classification\n";
  std::cout<<"geometric_r_0.6,25,"<<10.0*std::pow(0.6,24)<<","<<geo<<","<<geo_ref<<","<<geo_ref-geo<<",convergent geometric series\n";
  std::cout<<"harmonic,10000,"<<1.0/10000.0<<","<<harm<<",,,divergent despite terms approaching zero\n";
}
