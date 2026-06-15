#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double geometric_power_series(double x, int n_terms){
  double total = 0.0;
  for(int n=0; n<n_terms; n++){ total += std::pow(x, n); }
  return total;
}

int main(){
  std::vector<double> xs = {0.25, 0.75, 1.25};
  std::vector<int> terms = {5, 20, 10};

  std::cout << std::fixed << std::setprecision(12);
  std::cout << "function_name,center,x_value,n_terms,partial_sum,reference_value,absolute_error,convergence_status,warning\n";

  for(size_t i=0; i<xs.size(); ++i){
    double x = xs[i];
    int n_terms = terms[i];
    double partial = geometric_power_series(x, n_terms);
    bool converges = std::abs(x) < 1.0;

    if(converges){
      double reference = 1.0 / (1.0 - x);
      std::cout << "1/(1-x),0.0," << x << "," << n_terms << "," << partial << "," << reference << "," << std::abs(reference - partial) << ",inside radius of convergence,\n";
    } else {
      std::cout << "1/(1-x),0.0," << x << "," << n_terms << "," << partial << ",,,outside radius of convergence,Power series does not converge for this x value.\n";
    }
  }
}
