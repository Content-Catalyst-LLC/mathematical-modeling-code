#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double simulate_model(const std::string& form_key) {
    double stock = 80.0;
    const double carrying_capacity = 120.0;
    const double extraction_rate = 0.12;
    const double growth_rate = 0.08;
    const double fixed_loss = 5.8;
    const double critical_threshold = 55.0;

    for (int year = 0; year < 10; ++year) {
        if (form_key == "linear_decline") {
            stock = std::max(0.0, stock - fixed_loss);
        } else if (form_key == "proportional_decline") {
            stock = std::max(0.0, stock - extraction_rate * stock);
        } else if (form_key == "logistic_recovery") {
            const double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
            const double extraction = extraction_rate * stock;
            stock = std::max(0.0, stock + growth - extraction);
        } else if (form_key == "threshold_shift") {
            if (stock < critical_threshold) {
                stock = std::max(0.0, stock - 1.6 * extraction_rate * stock);
            } else {
                stock = std::max(0.0, stock - extraction_rate * stock);
            }
        }
    }

    return stock;
}

int main() {
    std::vector<std::string> forms = {
        "linear_decline",
        "proportional_decline",
        "logistic_recovery",
        "threshold_shift"
    };

    std::vector<double> outputs;
    std::cout << "model_form,projected_stock,below_threshold\n";

    for (const auto& form : forms) {
        const double y = simulate_model(form);
        outputs.push_back(y);
        std::cout << std::fixed << std::setprecision(6)
                  << form << "," << y << "," << (y < 45.0 ? "true" : "false") << "\n";
    }

    const auto minmax = std::minmax_element(outputs.begin(), outputs.end());
    std::cerr << "structural_spread=" << (*minmax.second - *minmax.first) << "\n";

    return 0;
}
