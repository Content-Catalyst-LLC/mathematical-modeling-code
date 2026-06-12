#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    std::string structure;
    double initial_stock;
    double capacity;
    double inflow;
    double demand;
    double loss_rate;
    double feedback_strength;
    int periods;
};

struct Row {
    int period;
    double stock;
    double shortage;
    double overflow;
};

class StructureResourceModel {
public:
    explicit StructureResourceModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_stock < 0.0) throw std::invalid_argument("stock must be nonnegative");
        if (scenario_.initial_stock > scenario_.capacity) throw std::invalid_argument("stock exceeds capacity");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double stock = scenario_.initial_stock;
        double demand = scenario_.demand;

        for (int period = 0; period <= scenario_.periods; ++period) {
            const double losses = scenario_.loss_rate * stock;
            const double raw_next = stock + scenario_.inflow - demand - losses;
            const double shortage = std::max(0.0, -raw_next);
            const double overflow = std::max(0.0, raw_next - scenario_.capacity);
            double next_stock = raw_next;

            if (scenario_.structure == "constrained" || scenario_.structure == "feedback") {
                next_stock = std::min(scenario_.capacity, std::max(0.0, raw_next));
            }

            rows.push_back({period, stock, shortage, overflow});

            if (scenario_.structure == "feedback") {
                demand = std::max(0.0, demand - scenario_.feedback_strength * shortage);
            }

            stock = next_stock;
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario scenario{"cpp_feedback", "feedback", 40.0, 60.0, 3.0, 7.0, 0.050, 0.20, 60};
    StructureResourceModel model(scenario);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    double total_overflow = 0.0;
    for (const auto& row : rows) {
        total_shortage += row.shortage;
        total_overflow += row.overflow;
    }

    std::cout << std::fixed << std::setprecision(6)
              << "cpp structure=" << scenario.structure
              << " final_stock=" << rows.back().stock
              << " total_shortage=" << total_shortage
              << " total_overflow=" << total_overflow << "\n";
    return 0;
}
