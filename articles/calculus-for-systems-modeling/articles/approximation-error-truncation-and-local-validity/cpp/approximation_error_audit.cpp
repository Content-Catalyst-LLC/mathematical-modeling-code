#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double factorial_int(int n){
  double result = 1.0;
  for(int i=2; i<=n; ++i){ result *= static_cast<double>(i); }
  return result;
}

double taylor_exp(double x, int order){
  double total = 0.0;
  for(int n=0; n<=order; ++n){ total += std::pow(x, n) / factorial_int(n); }
  return total;
}

int main(){
  std::vector<double> xs = {0.5, 1.0, 3.0};
  std::vector<int> orders = {2, 10, 10};

  std::cout << std::fixed << std::setprecision(12);
  std::cout << "method,function_name,center,x_value,order,approximation,reference_value,absolute_error,relative_error,warning\n";
  for(size_t i=0; i<xs.size(); ++i){
    double x = xs[i];
    int order = orders[i];
    double approx = taylor_exp(x, order);
    double reference = std::exp(x);
    double abs_err = std::abs(reference-approx);
    double rel_err = abs_err / std::abs(reference);
    std::string warning = std::abs(x) <= 2.0 ? "" : "Evaluation is far from the expansion center; review local validity.";
    std::cout << "Maclaurin truncation,exp(x),0.0," << x << "," << order << "," << approx << "," << reference << "," << abs_err << "," << rel_err << "," << warning << "\n";
  }
}
