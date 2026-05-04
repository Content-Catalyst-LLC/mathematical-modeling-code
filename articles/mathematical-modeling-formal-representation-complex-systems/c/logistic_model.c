#include <stdio.h>

int main(void) {
    const int time_steps = 80;
    double state[time_steps];
    double growth_rate = 0.18;
    double carrying_capacity = 100.0;

    state[0] = 10.0;

    for (int t = 1; t < time_steps; t++) {
        state[t] = state[t - 1] + growth_rate * state[t - 1] * (1.0 - state[t - 1] / carrying_capacity);
    }

    printf("Final state: %.3f\n", state[time_steps - 1]);

    return 0;
}
