#include <cmath>
#include <iostream>
#include <string>

int main() {
    const double a = 0.80, b = 0.15, c = 0.20, d = 0.90;
    const double trace = a + d;
    const double det = a * d - b * c;
    const double disc = trace * trace - 4.0 * det;
    const double root = std::sqrt(disc);
    const double lambda1 = (trace + root) / 2.0;
    const double lambda2 = (trace - root) / 2.0;
    const double dominant = std::max(std::abs(lambda1), std::abs(lambda2));
    std::cout << "model_name,rank,determinant,dominant_eigenvalue,warning\n";
    std::cout << "two_component_transition_model,2," << det << "," << dominant
              << ",Matrix interpretation depends on entry meaning and scale.\n";
    return 0;
}
