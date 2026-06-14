#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double system_response(double x) {
    return std::exp(0.2 * x);
}

double exact_derivative(double x) {
    return 0.2 * std::exp(0.2 * x);
}

double difference_quotient(double x, double h) {
    return (system_response(x + h) - system_response(x)) / h;
}

int main() {
    const double x = 5.0;
    const double exact = exact_derivative(x);
    const std::vector<double> h_values = {1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001};

    std::cout << "function_name,x,h,estimate,exact_value,absolute_error\n";
    for (const auto h : h_values) {
        const double estimate = difference_quotient(x, h);
        std::cout << "exp(0.2x),"
                  << std::fixed << std::setprecision(6) << x << ","
                  << h << ","
                  << std::setprecision(12) << estimate << ","
                  << exact << ","
                  << std::fabs(estimate - exact) << "\n";
    }

    return 0;
}
