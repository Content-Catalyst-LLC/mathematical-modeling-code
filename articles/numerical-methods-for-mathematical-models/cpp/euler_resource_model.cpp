#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double derivative(double stock, double growth_rate, double carrying_capacity, double extraction) {
    return growth_rate * stock * (1.0 - stock / carrying_capacity) - extraction;
}

double run_euler(double step_size) {
    double stock = 70.0;
    const double growth_rate = 0.18;
    const double carrying_capacity = 100.0;
    const double extraction = 6.0;
    const double horizon = 50.0;
    const int steps = static_cast<int>(std::round(horizon / step_size));

    for (int i = 0; i < steps; ++i) {
        stock = stock + step_size * derivative(stock, growth_rate, carrying_capacity, extraction);
        stock = std::max(0.0, stock);
    }

    return stock;
}

int main() {
    std::vector<double> step_sizes = {1.0, 0.5, 0.25, 0.1};
    const double reference = run_euler(0.1);

    std::cout << "step_size,final_stock,difference_from_finest\n";

    for (double h : step_sizes) {
        double final_stock = run_euler(h);
        std::cout << std::fixed << std::setprecision(6)
                  << h << "," << final_stock << "," << std::abs(final_stock - reference) << "\n";
    }

    return 0;
}
