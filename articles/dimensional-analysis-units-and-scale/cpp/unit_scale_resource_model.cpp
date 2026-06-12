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
    double inflow_per_day;
    double demand_per_day;
    double loss_rate_per_day;
    double delta_t_days;
    int periods;
};

struct Row {
    int period;
    double storage;
    double storage_fraction;
    double shortage;
};

class UnitScaleResourceModel {
public:
    explicit UnitScaleResourceModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_storage < 0.0) throw std::invalid_argument("storage must be nonnegative");
        if (scenario_.initial_storage > scenario_.capacity) throw std::invalid_argument("storage exceeds capacity");
        if (scenario_.loss_rate_per_day < 0.0 || scenario_.loss_rate_per_day > 1.0) throw std::invalid_argument("loss rate out of domain");
        if (scenario_.delta_t_days <= 0.0) throw std::invalid_argument("time step must be positive");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double storage = scenario_.initial_storage;

        for (int period = 0; period <= scenario_.periods; ++period) {
            const double inflow_volume = scenario_.delta_t_days * scenario_.inflow_per_day;
            const double demand_volume = scenario_.delta_t_days * scenario_.demand_per_day;
            const double loss_volume = scenario_.delta_t_days * scenario_.loss_rate_per_day * storage;
            const double raw_next = storage + inflow_volume - demand_volume - loss_volume;
            const double shortage = std::max(0.0, -raw_next);
            const double next_storage = std::min(scenario_.capacity, std::max(0.0, raw_next));

            rows.push_back({period, storage, next_storage / scenario_.capacity, shortage});
            storage = next_storage;
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario scenario{"cpp_daily_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 1.0, 60};
    UnitScaleResourceModel model(scenario);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    double min_fraction = 1.0;
    double max_fraction = 0.0;
    for (const auto& row : rows) {
        total_shortage += row.shortage;
        min_fraction = std::min(min_fraction, row.storage_fraction);
        max_fraction = std::max(max_fraction, row.storage_fraction);
    }

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_storage=" << rows.back().storage
              << " min_fraction=" << min_fraction
              << " max_fraction=" << max_fraction
              << " total_shortage=" << total_shortage << "\n";
    return 0;
}
