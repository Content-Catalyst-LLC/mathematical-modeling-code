#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double linear_model(double x) {
    return 10.0 + 2.0 * x;
}

double exponential_model(double x) {
    return 10.0 * std::exp(0.18 * x);
}

double logistic_model(double x) {
    return 100.0 / (1.0 + std::exp(-0.75 * (x - 5.0)));
}

double threshold_model(double x) {
    return x < 5.0 ? 20.0 : 80.0;
}

int main() {
    const double x = 10.0;
    std::cout << "model,final_value\n";
    std::cout << "linear_growth," << std::fixed << std::setprecision(6) << linear_model(x) << "\n";
    std::cout << "exponential_growth," << exponential_model(x) << "\n";
    std::cout << "logistic_growth," << logistic_model(x) << "\n";
    std::cout << "threshold_response," << threshold_model(x) << "\n";
    return 0;
}
