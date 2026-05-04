#include <stdio.h>

int main(void) {
    const int steps = 300;
    const double dt = 0.1;
    const double rate = 0.20;
    const double capacity = 100.0;

    double state[steps];
    state[0] = 10.0;

    for (int i = 1; i < steps; i++) {
        double derivative = rate * state[i - 1] * (1.0 - state[i - 1] / capacity);
        state[i] = state[i - 1] + derivative * dt;
    }

    printf("Final state: %.6f\n", state[steps - 1]);

    return 0;
}
