#include <iostream>
#include <vector>

std::vector<double> simulate_logistic(double initial_state, double rate, double capacity, double dt, int steps) {
    std::vector<double> state(steps, 0.0);
    state[0] = initial_state;

    for (int i = 1; i < steps; ++i) {
        double derivative = rate * state[i - 1] * (1.0 - state[i - 1] / capacity);
        state[i] = state[i - 1] + derivative * dt;
    }

    return state;
}

int main() {
    auto state = simulate_logistic(10.0, 0.20, 100.0, 0.1, 300);
    std::cout << "Final state: " << state.back() << "\n";
    return 0;
}
