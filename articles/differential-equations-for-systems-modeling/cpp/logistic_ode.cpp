#include <iostream>
#include <vector>

double logistic_rate(double state, double growth_rate, double capacity) {
    return growth_rate * state * (1.0 - state / capacity);
}

std::vector<double> simulate_logistic(double initial_state, double growth_rate, double capacity, double dt, int steps) {
    std::vector<double> state(steps, 0.0);
    state[0] = initial_state;

    for (int i = 1; i < steps; ++i) {
        double derivative = logistic_rate(state[i - 1], growth_rate, capacity);
        state[i] = state[i - 1] + derivative * dt;
    }

    return state;
}

int main() {
    auto state = simulate_logistic(10.0, 0.20, 100.0, 0.1, 300);

    std::cout << "Final state: " << state.back() << "\n";

    return 0;
}
