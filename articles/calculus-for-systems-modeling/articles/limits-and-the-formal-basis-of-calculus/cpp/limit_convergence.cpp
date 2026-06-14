#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double f(double x) {
    return std::exp(0.2 * x);
}

double exact_derivative(double x) {
    return 0.2 * std::exp(0.2 * x);
}

double forward_difference(double x, double h) {
    return (f(x + h) - f(x)) / h;
}

double central_difference(double x, double h) {
    return (f(x + h) - f(x - h)) / (2.0 * h);
}

double richardson(double central_h, double central_h2) {
    return (4.0 * central_h2 - central_h) / 3.0;
}

int main() {
    const double x = 5.0;
    const double exact = exact_derivative(x);
    const std::vector<double> h_values = {1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125};

    std::cout << "method,x,h,estimate,exact,absolute_error\n";

    for (const auto h : h_values) {
        const double fd = forward_difference(x, h);
        const double cd = central_difference(x, h);
        const double cd2 = central_difference(x, h / 2.0);
        const double rich = richardson(cd, cd2);

        std::cout << std::setprecision(12)
                  << "forward_difference," << x << "," << h << "," << fd << "," << exact << "," << std::fabs(fd - exact) << "\n"
                  << "central_difference," << x << "," << h << "," << cd << "," << exact << "," << std::fabs(cd - exact) << "\n"
                  << "richardson_central," << x << "," << h << "," << rich << "," << exact << "," << std::fabs(rich - exact) << "\n";
    }

    return 0;
}
