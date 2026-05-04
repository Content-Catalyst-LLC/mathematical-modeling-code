#include <array>
#include <iostream>

int main() {
    std::array<std::array<double, 3>, 3> A = {{
        {{0.82, 0.10, 0.08}},
        {{0.12, 0.76, 0.12}},
        {{0.06, 0.18, 0.76}}
    }};

    std::array<double, 3> x = {{0.70, 0.20, 0.10}};
    std::array<double, 3> y = {{0.0, 0.0, 0.0}};

    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            y[i] += A[i][j] * x[j];
        }
    }

    std::cout << "Transformed state: "
              << y[0] << " " << y[1] << " " << y[2] << "\n";

    return 0;
}
