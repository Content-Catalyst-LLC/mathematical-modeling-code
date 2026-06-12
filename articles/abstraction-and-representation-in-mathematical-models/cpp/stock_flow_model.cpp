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
    int periods;
};

struct Row {
    int period;
    double stock;
    double shortage;
};

class StockFlowModel {
public:
    explicit StockFlowModel(Scenario scenario) : scenario_(std::move(scenario)) {
        if (scenario_.capacity <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (scenario_.initial_stock < 0.0) throw std::invalid_argument("stock must be nonnegative");
        if (scenario_.initial_stock > scenario_.capacity) throw std::invalid_argument("stock exceeds capacity");
    }

    std::vector<Row> simulate() const {
        std::vector<Row> rows;
        double stock = scenario_.initial_stock;

        for (int period = 0; period <= scenario_.periods; ++period) {
            const double losses = scenario_.loss_rate * stock;
            const double shortage = std::max(0.0, scenario_.demand + losses - (stock + scenario_.inflow));
            rows.push_back({period, stock, shortage});
            stock = std::min(scenario_.capacity, std::max(0.0, stock + scenario_.inflow - scenario_.demand - losses));
        }

        return rows;
    }

private:
    Scenario scenario_;
};

int main() {
    Scenario baseline{"cpp_aggregate_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 60};
    StockFlowModel model(baseline);
    const auto rows = model.simulate();

    double total_shortage = 0.0;
    for (const auto& row : rows) total_shortage += row.shortage;

    std::cout << std::fixed << std::setprecision(6)
              << "cpp final_stock=" << rows.back().stock
              << " total_shortage=" << total_shortage << "\n";
    return 0;
}
