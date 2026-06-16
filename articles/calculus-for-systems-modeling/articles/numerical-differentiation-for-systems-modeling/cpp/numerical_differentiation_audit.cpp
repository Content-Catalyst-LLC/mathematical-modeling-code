#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

double signal_function(double x){ return std::sin(x) + 0.1 * x * x; }
double true_derivative(double x){ return std::cos(x) + 0.2 * x; }

int main(){
  const double start = 0.0, stop = 10.0, h = 0.1;
  const int n = static_cast<int>(std::round((stop - start) / h));
  std::vector<double> xs(n + 1), values(n + 1);

  for(int i=0; i<=n; i++){
    xs[i] = start + i * h;
    values[i] = signal_function(xs[i]);
  }

  const double nan = std::numeric_limits<double>::quiet_NaN();
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "index,x,value,true_derivative,forward_difference,backward_difference,central_difference,central_absolute_error,step_size,warning\n";
  for(int i=0; i<=n; i++){
    double forward = nan, backward = nan, central = nan, err = nan;
    if(i < n) forward = (values[i+1] - values[i]) / h;
    if(i > 0) backward = (values[i] - values[i-1]) / h;
    if(i > 0 && i < n){
      central = (values[i+1] - values[i-1]) / (2.0*h);
      err = std::abs(central - true_derivative(xs[i]));
    }
    std::cout << i << "," << xs[i] << "," << values[i] << "," << true_derivative(xs[i]) << "," << forward << "," << backward << "," << central << "," << err << "," << h << ",Numerical derivatives depend on step size formula choice boundary handling smoothness and noise.\n";
  }
}
