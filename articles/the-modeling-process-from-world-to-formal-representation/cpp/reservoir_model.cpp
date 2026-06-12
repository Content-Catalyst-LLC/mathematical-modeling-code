#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double initial_storage;
    double capacity;
    double base_inflow;
    double base_demand;
    double demand_growth;
    double loss_rate;
    int periods;
};

struct Row {
    int period;
    double storage;
    double shortage;
};

class ReservoirModel {
public:
    explicit ReservoirModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_storage < 0.0) throw std::invalid_argument("storage must be nonnegative");
        if (scenario_.initial_storage > scenario_.capacity) throw std::invalid_argument("storage exceeds capacity");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double storage = scenario_.initial_storage;

        for (int period = 0; period <= scenario_.periods; ++period) {
            double demand = scenario_.base_demand;
            for (int i = 0; i < period; ++i) demand *= (1.0 + scenario_.demand_growth);

            const double losses = scenario_.loss_rate * storage;
            const double shortage = std::max(0.0, demand + losses - (storage + scenario_.base_inflow));
            rows.push_back({period, storage, shortage});
            storage = std::min(scenario_.capacity, std::max(0.0, storage + scenario_.base_inflow - demand - losses));
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario baseline{"cpp_baseline", 80.0, 100.0, 8.0, 6.0, 0.010, 0.015, 60};
    ReservoirModel model(baseline);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    for (const auto& row : rows) total_shortage += row.shortage;

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_storage=" << rows.back().storage
              << " total_shortage=" << total_shortage << "\n";
    return 0;
}
