#include <cmath>
#include <iomanip>
#include <iostream>

double geometric_sum(double a, double r, int n){
  double total = 0.0;
  for(int i=0;i<n;i++){ total += a * std::pow(r, i); }
  return total;
}

double p_series_sum(double p, int n){
  double total = 0.0;
  for(int i=1;i<=n;i++){ total += 1.0 / std::pow(static_cast<double>(i), p); }
  return total;
}

int main(){
  double geo = geometric_sum(10.0, 0.6, 25);
  double geo_ref = 10.0 / (1.0 - 0.6);
  double p125 = p_series_sum(1.25, 10000);
  double p075 = p_series_sum(0.75, 10000);

  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"series_name,test_used,n_terms,partial_sum,last_term,test_result,estimated_error\n";
  std::cout<<"geometric_r_0.6,geometric-series test,25,"<<geo<<","<<10.0*std::pow(0.6,24)<<",converges by geometric-series test,"<<geo_ref-geo<<"\n";
  std::cout<<"p_series_1.25,p-series test,10000,"<<p125<<","<<1.0/std::pow(10000.0,1.25)<<",converges,\n";
  std::cout<<"p_series_0.75,p-series test,10000,"<<p075<<","<<1.0/std::pow(10000.0,0.75)<<",diverges,\n";
}
