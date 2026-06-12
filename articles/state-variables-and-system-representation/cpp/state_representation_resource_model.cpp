#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    std::string representation;
    double initial_storage;
    double initial_demand;
    double initial_condition;
    double capacity;
    double inflow;
    double loss_rate;
    double demand_response;
    double condition_decay;
    int periods;
};

struct Row {
    int period;
    double storage;
    double demand;
    double condition;
    double shortage;
};

class StateRepresentationModel {
public:
    explicit StateRepresentationModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_storage < 0.0) throw std::invalid_argument("storage must be nonnegative");
        if (scenario_.initial_storage > scenario_.capacity) throw std::invalid_argument("storage exceeds capacity");
        if (scenario_.initial_condition < 0.0 || scenario_.initial_condition > 1.0) throw std::invalid_argument("condition out of domain");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double storage = scenario_.initial_storage;
        double demand = scenario_.initial_demand;
        double condition = scenario_.initial_condition;

        for (int period = 0; period <= scenario_.periods; ++period) {
            double effective_loss_rate = scenario_.loss_rate;
            if (scenario_.representation == "condition_aware") {
                effective_loss_rate = scenario_.loss_rate * (1.0 + (1.0 - condition));
            }

            const double losses = effective_loss_rate * storage;
            const double raw_next = storage + scenario_.inflow - demand - losses;
            const double shortage = std::max(0.0, -raw_next);

            rows.push_back({period, storage, demand, condition, shortage});

            if (scenario_.representation == "adaptive_demand" || scenario_.representation == "condition_aware") {
                demand = std::max(0.0, demand - scenario_.demand_response * shortage);
            }

            if (scenario_.representation == "condition_aware") {
                condition = std::max(0.0, condition - scenario_.condition_decay * shortage);
            }

            storage = std::min(scenario_.capacity, std::max(0.0, raw_next));
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario scenario{"cpp_condition_aware", "condition_aware", 45.0, 8.0, 0.85, 80.0, 4.0, 0.020, 0.20, 0.002, 60};
    StateRepresentationModel model(scenario);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    for (const auto& row : rows) {
        total_shortage += row.shortage;
    }

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_storage=" << rows.back().storage
              << " final_demand=" << rows.back().demand
              << " final_condition=" << rows.back().condition
              << " total_shortage=" << total_shortage << "\n";
    return 0;
}
