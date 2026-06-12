#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double initial_storage;
    double initial_demand;
    double capacity;
    double inflow;
    double loss_rate;
    double demand_response;
    int periods;
    bool adaptive_demand;
};

struct Row {
    int period;
    double storage;
    double demand;
    double shortage;
    double overflow;
};

class RecurrenceResourceModel {
public:
    explicit RecurrenceResourceModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_storage < 0.0) throw std::invalid_argument("storage must be nonnegative");
        if (scenario_.initial_storage > scenario_.capacity) throw std::invalid_argument("storage exceeds capacity");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double storage = scenario_.initial_storage;
        double demand = scenario_.initial_demand;

        for (int period = 0; period <= scenario_.periods; ++period) {
            const double raw_next = storage + scenario_.inflow - demand - scenario_.loss_rate * storage;
            const double shortage = std::max(0.0, -raw_next);
            const double overflow = std::max(0.0, raw_next - scenario_.capacity);
            const double next_storage = std::min(scenario_.capacity, std::max(0.0, raw_next));

            rows.push_back({period, storage, demand, shortage, overflow});

            if (scenario_.adaptive_demand) {
                demand = std::max(0.0, demand - scenario_.demand_response * shortage);
            }

            storage = next_storage;
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario scenario{"cpp_adaptive", 45.0, 10.0, 80.0, 4.0, 0.020, 0.20, 60, true};
    RecurrenceResourceModel model(scenario);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    double total_overflow = 0.0;
    for (const auto& row : rows) {
        total_shortage += row.shortage;
        total_overflow += row.overflow;
    }

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_storage=" << rows.back().storage
              << " final_demand=" << rows.back().demand
              << " total_shortage=" << total_shortage
              << " total_overflow=" << total_overflow
              << "\n";
    return 0;
}
