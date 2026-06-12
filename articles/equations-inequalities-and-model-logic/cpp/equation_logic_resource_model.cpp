#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double initial_stock;
    double capacity;
    double inflow;
    double demand;
    double loss_rate;
    double low_storage_threshold;
    double demand_reduction;
    int periods;
};

struct Row {
    int period;
    double stock;
    double shortage;
    bool logic_active;
};

class EquationLogicResourceModel {
public:
    explicit EquationLogicResourceModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_stock < 0.0) throw std::invalid_argument("stock must be nonnegative");
        if (scenario_.initial_stock > scenario_.capacity) throw std::invalid_argument("stock exceeds capacity");
        if (scenario_.loss_rate < 0.0 || scenario_.loss_rate > 1.0) throw std::invalid_argument("loss rate out of domain");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double stock = scenario_.initial_stock;
        double demand = scenario_.demand;

        for (int period = 0; period <= scenario_.periods; ++period) {
            const double losses = scenario_.loss_rate * stock;
            const double raw_next = stock + scenario_.inflow - demand - losses;
            const double shortage = std::max(0.0, -raw_next);
            const bool logic_active = stock < scenario_.low_storage_threshold;

            rows.push_back({period, stock, shortage, logic_active});

            if (logic_active) {
                demand = std::max(0.0, demand - scenario_.demand_reduction);
            }

            stock = std::min(scenario_.capacity, std::max(0.0, raw_next));
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario scenario{"cpp_constraint_stress", 40.0, 60.0, 3.0, 7.0, 0.050, 25.0, 1.0, 60};
    EquationLogicResourceModel model(scenario);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    int activations = 0;
    for (const auto& row : rows) {
        total_shortage += row.shortage;
        if (row.logic_active) {
            activations += 1;
        }
    }

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_stock=" << rows.back().stock
              << " total_shortage=" << total_shortage
              << " logic_activations=" << activations << "\n";
    return 0;
}
