#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Scenario {
    std::string key;
    std::string form;
    std::string scenario;
    double extraction_multiplier;
    double shock;
};

double simulate(const std::string& form, double extraction_multiplier, double shock) {
    double stock = 80.0;
    const double carrying_capacity = 120.0;
    const double growth_rate = 0.08;
    const double extraction_rate = 0.12 * extraction_multiplier;
    const double fixed_loss = 5.8 * extraction_multiplier;
    const double critical_threshold = 55.0;

    for (int year = 0; year < 10; ++year) {
        if (form == "linear_decline") {
            stock = std::max(0.0, stock - fixed_loss - shock * stock);
        } else if (form == "logistic_recovery") {
            const double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
            const double extraction = extraction_rate * stock;
            stock = std::max(0.0, stock + growth - extraction - shock * stock);
        } else if (form == "threshold_shift") {
            if (stock < critical_threshold) {
                stock = std::max(0.0, stock - 1.6 * extraction_rate * stock - shock * stock);
            } else {
                stock = std::max(0.0, stock - extraction_rate * stock - shock * stock);
            }
        }
    }

    return stock;
}

int main() {
    std::vector<Scenario> scenarios = {
        {"linear_baseline", "linear_decline", "baseline", 1.0, 0.00},
        {"linear_stress", "linear_decline", "stress", 1.25, 0.05},
        {"dynamic_baseline", "logistic_recovery", "baseline", 1.0, 0.00},
        {"dynamic_stress", "logistic_recovery", "stress", 1.25, 0.05},
        {"threshold_baseline", "threshold_shift", "baseline", 1.0, 0.00},
        {"threshold_stress", "threshold_shift", "stress", 1.25, 0.05}
    };

    std::vector<double> outputs;
    std::cout << "key,model_form,scenario,projected_stock,below_threshold\n";

    for (const auto& s : scenarios) {
        const double y = simulate(s.form, s.extraction_multiplier, s.shock);
        outputs.push_back(y);
        std::cout << std::fixed << std::setprecision(6)
                  << s.key << "," << s.form << "," << s.scenario << "," << y << ","
                  << (y < 45.0 ? "true" : "false") << "\n";
    }

    const auto minmax = std::minmax_element(outputs.begin(), outputs.end());
    std::cerr << "robustness_spread=" << (*minmax.second - *minmax.first) << "\n";

    return 0;
}
