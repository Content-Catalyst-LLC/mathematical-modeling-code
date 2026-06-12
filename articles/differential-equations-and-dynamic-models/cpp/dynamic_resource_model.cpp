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
    double inflow_rate;
    double demand_rate;
    double loss_rate;
    double dt;
    double horizon;
};

struct Row {
    int step;
    double time;
    double storage;
    double rate;
    double shortage;
    double overflow;
};

class DynamicResourceModel {
public:
    explicit DynamicResourceModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_storage < 0.0) throw std::invalid_argument("storage must be nonnegative");
        if (scenario_.initial_storage > scenario_.capacity) throw std::invalid_argument("storage exceeds capacity");
        if (scenario_.dt <= 0.0) throw std::invalid_argument("time step must be positive");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double storage = scenario_.initial_storage;
        double time = 0.0;
        const int steps = static_cast<int>(scenario_.horizon / scenario_.dt);

        for (int step = 0; step <= steps; ++step) {
            const double rate = scenario_.inflow_rate - scenario_.demand_rate - scenario_.loss_rate * storage;
            const double raw_next = storage + scenario_.dt * rate;
            const double shortage = std::max(0.0, -raw_next);
            const double overflow = std::max(0.0, raw_next - scenario_.capacity);
            const double next_storage = std::min(scenario_.capacity, std::max(0.0, raw_next));

            rows.push_back({step, time, storage, rate, shortage, overflow});

            storage = next_storage;
            time += scenario_.dt;
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario scenario{"cpp_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 0.25, 60.0};
    DynamicResourceModel model(scenario);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    double total_overflow = 0.0;
    for (const auto& row : rows) {
        total_shortage += row.shortage;
        total_overflow += row.overflow;
    }

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_storage=" << rows.back().storage
              << " total_shortage=" << total_shortage
              << " total_overflow=" << total_overflow
              << "\n";
    return 0;
}
