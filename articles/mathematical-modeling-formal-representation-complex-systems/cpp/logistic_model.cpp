#include <iostream>
#include <vector>

std::vector<double> simulate_logistic(double initial_state, double growth_rate, double carrying_capacity, int time_steps) {
    std::vector<double> state(time_steps, 0.0);
    state[0] = initial_state;

    for (int t = 1; t < time_steps; ++t) {
        state[t] = state[t - 1] + growth_rate * state[t - 1] * (1.0 - state[t - 1] / carrying_capacity);
    }

    return state;
}

int main() {
    auto state = simulate_logistic(10.0, 0.18, 100.0, 80);

    std::cout << "Final state: " << state.back() << "\n";

    return 0;
}
