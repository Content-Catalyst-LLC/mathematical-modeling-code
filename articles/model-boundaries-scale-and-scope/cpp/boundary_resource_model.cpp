#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    std::string boundary_version;
    double initial_stock;
    double capacity;
    double inflow;
    double demand;
    double loss_rate;
    double policy_savings;
    int periods;
};

struct Row {
    int period;
    double stock;
    double shortage;
};

class BoundaryResourceModel {
public:
    explicit BoundaryResourceModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_stock < 0.0) throw std::invalid_argument("stock must be nonnegative");
        if (scenario_.initial_stock > scenario_.capacity) throw std::invalid_argument("stock exceeds capacity");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double stock = scenario_.initial_stock;

        for (int period = 0; period <= scenario_.periods; ++period) {
            const double effective_demand = std::max(0.0, scenario_.demand - scenario_.policy_savings);
            const double losses = scenario_.loss_rate * stock;
            const double shortage = std::max(0.0, effective_demand + losses - (stock + scenario_.inflow));
            rows.push_back({period, stock, shortage});
            stock = std::min(scenario_.capacity, std::max(0.0, stock + scenario_.inflow - effective_demand - losses));
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario baseline{"cpp_policy_expanded", "policy_expanded", 80.0, 100.0, 5.0, 6.0, 0.015, 1.5, 60};
    BoundaryResourceModel model(baseline);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    for (const auto& row : rows) total_shortage += row.shortage;

    std::cout << std::fixed << std::setprecision(6)
              << "cpp boundary=" << baseline.boundary_version
              << " final_stock=" << rows.back().stock
              << " total_shortage=" << total_shortage << "\n";
    return 0;
}
