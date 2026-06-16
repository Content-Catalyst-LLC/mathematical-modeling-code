#include <cmath>
#include <iostream>

double exponential_population(double n0, double r, double t) {
  return n0 * std::exp(r * t);
}

double logistic_population(double n0, double r, double k, double t) {
  return k / (1.0 + ((k - n0) / n0) * std::exp(-r * t));
}

int main() {
  double n0 = 100.0, r = 0.08, k = 1000.0;
  std::cout << "time,exponential,logistic\n";
  for (int t = 0; t <= 40; ++t) {
    std::cout << t << "," << exponential_population(n0, r, t) << "," << logistic_population(n0, r, k, t) << "\n";
  }
  return 0;
}
