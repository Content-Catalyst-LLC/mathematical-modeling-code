#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct StateRow {
    int step;
    double time;
    double state;
};

class LogisticModel {
public:
    LogisticModel(std::string name, double initial, double growth, double capacity, double dt, int steps)
        : name_(std::move(name)), initial_(initial), growth_(growth), capacity_(capacity), dt_(dt), steps_(steps) {
        if (initial_ < 0.0) throw std::invalid_argument("initial state must be nonnegative");
        if (capacity_ <= 0.0) throw std::invalid_argument("capacity must be positive");
        if (dt_ <= 0.0) throw std::invalid_argument("dt must be positive");
        if (steps_ < 1) throw std::invalid_argument("steps must be positive");
    }

    std::vector<StateRow> simulate_rk4() const {
        std::vector<StateRow> rows;
        rows.reserve(static_cast<std::size_t>(steps_ + 1));
        double x = initial_;

        for (int step = 0; step <= steps_; ++step) {
            rows.push_back({step, step * dt_, x});
            const double k1 = derivative(x);
            const double k2 = derivative(x + 0.5 * dt_ * k1);
            const double k3 = derivative(x + 0.5 * dt_ * k2);
            const double k4 = derivative(x + dt_ * k3);
            x = std::max(0.0, x + (dt_ / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4));
        }
        return rows;
    }

private:
    double derivative(double x) const {
        return growth_ * x * (1.0 - x / capacity_);
    }

    std::string name_;
    double initial_;
    double growth_;
    double capacity_;
    double dt_;
    int steps_;
};

int main() {
    LogisticModel model("cpp_baseline", 10.0, 0.35, 100.0, 0.1, 160);
    const auto rows = model.simulate_rk4();
    std::cout << std::fixed << std::setprecision(6)
              << "C++ RK4 final_state=" << rows.back().state << "\n";
    return 0;
}
