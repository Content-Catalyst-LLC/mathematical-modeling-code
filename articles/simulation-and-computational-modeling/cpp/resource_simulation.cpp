#include <algorithm>
#include <iomanip>
#include <iostream>

int main() {
    double stock = 70.0;
    const double growth_rate = 0.18;
    const double capacity = 100.0;
    const double extraction = 6.0;
    const int steps = 20;

    std::cout << "step,resource_stock\n";

    for (int step = 0; step <= steps; ++step) {
        std::cout << step << "," << std::fixed << std::setprecision(6) << stock << "\n";
        const double growth = growth_rate * stock * (1.0 - stock / capacity);
        stock = std::max(0.0, stock + growth - extraction);
    }

    return 0;
}
