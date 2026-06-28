#include <cmath>
#include <iostream>

int main() {
    double a = 3.0, b = 1.0, c = 2.0, d = 4.0;
    double y1 = 7.0, y2 = 8.0;
    double det = a * d - b * c;

    std::cout << "det(A) = " << det << "\n";

    if (std::abs(det) < 1e-12) {
        std::cout << "Matrix is singular or numerically near-singular.\n";
        return 1;
    }

    double x1 = (d * y1 - b * y2) / det;
    double x2 = (-c * y1 + a * y2) / det;

    double r1 = a * x1 + b * x2 - y1;
    double r2 = c * x1 + d * x2 - y2;
    double residual_norm = std::sqrt(r1 * r1 + r2 * r2);

    std::cout << "Recovered state: x1 = " << x1 << ", x2 = " << x2 << "\n";
    std::cout << "Residual norm: " << residual_norm << "\n";

    return 0;
}
