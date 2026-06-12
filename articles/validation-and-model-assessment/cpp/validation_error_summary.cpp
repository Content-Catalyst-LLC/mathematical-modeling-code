#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Observation {
    double observed;
    double predicted;
    std::string scenario;
};

int main() {
    std::vector<Observation> data = {
        {70.1, 70.8, "holdout"},
        {68.9, 69.7, "holdout"},
        {67.4, 68.3, "holdout"},
        {65.8, 66.9, "holdout"},
        {64.2, 65.1, "holdout"},
        {62.1, 63.8, "stress"},
        {60.4, 61.3, "stress"},
        {58.8, 59.9, "stress"}
    };

    double sum_abs = 0.0;
    double sum_sq = 0.0;
    double bias = 0.0;
    double max_abs = 0.0;

    for (const auto& item : data) {
        const double residual = item.observed - item.predicted;
        const double abs_error = std::abs(residual);
        sum_abs += abs_error;
        sum_sq += residual * residual;
        bias += residual;
        max_abs = std::max(max_abs, abs_error);
    }

    const double n = static_cast<double>(data.size());
    const double rmse = std::sqrt(sum_sq / n);
    const double mae = sum_abs / n;
    bias = bias / n;

    std::string fitness = "not_adequate_without_revision";
    if (rmse <= 1.25 && max_abs <= 2.0) {
        fitness = "adequate_for_scenario_screening";
    } else if (rmse <= 2.5) {
        fitness = "limited_use_requires_review";
    }

    std::cout << "rmse,mae,bias,max_abs_error,fitness\n";
    std::cout << std::fixed << std::setprecision(6)
              << rmse << "," << mae << "," << bias << "," << max_abs << "," << fitness << "\n";

    return 0;
}
