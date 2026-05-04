#include <cmath>
#include <iostream>

double trapezoid_integral(double start, double end, int intervals) {
    double width = (end - start) / intervals;
    double total = 0.0;

    for (int i = 1; i <= intervals; ++i) {
        double x0 = start + (i - 1) * width;
        double x1 = start + i * width;
        double y0 = std::sin(x0) + 1.5;
        double y1 = std::sin(x1) + 1.5;
        total += 0.5 * (y0 + y1) * width;
    }

    return total;
}

int main() {
    double estimate = trapezoid_integral(0.0, 10.0, 500);
    std::cout << "Trapezoid integral estimate: " << estimate << "\n";
    return 0;
}
