#include <cmath>
#include <functional>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double forward_difference(const std::function<double(double)> &f, double x, double h) {
    return (f(x + h) - f(x)) / h;
}

double backward_difference(const std::function<double(double)> &f, double x, double h) {
    return (f(x) - f(x - h)) / h;
}

double central_difference(const std::function<double(double)> &f, double x, double h) {
    return (f(x + h) - f(x - h)) / (2.0 * h);
}

void emit(const std::string &name, const std::function<double(double)> &f, double x0) {
    const std::vector<double> h_values = {1.0, 0.5, 0.25, 0.125, 0.0625};

    for (const auto h : h_values) {
        const double fwd = forward_difference(f, x0, h);
        const double bwd = backward_difference(f, x0, h);
        const double cen = central_difference(f, x0, h);
        const double gap = std::fabs(fwd - bwd);
        std::cout << name << "," << x0 << "," << h << ","
                  << fwd << "," << bwd << "," << cen << ","
                  << gap << "," << (gap > 0.5 ? "true" : "false") << "\n";
    }
}

int main() {
    auto smooth = [](double x) { return std::exp(0.2 * x); };
    auto kink = [](double x) { return std::fabs(x); };

    std::cout << std::fixed << std::setprecision(12);
    std::cout << "function_name,x0,h,forward,backward,central,one_sided_gap,kink_flag\n";
    emit("smooth_exp_response", smooth, 5.0);
    emit("kink_abs_response", kink, 0.0);
    return 0;
}
