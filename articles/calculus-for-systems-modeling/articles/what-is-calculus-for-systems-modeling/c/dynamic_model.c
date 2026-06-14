#include <stdio.h>
#include <stdlib.h>

double simulate(double initial_state, double rate, double capacity, double dt, int steps) {
    double state = initial_state;
    for (int i = 0; i < steps; ++i) {
        double derivative = rate * state * (1.0 - state / capacity);
        state = state + derivative * dt;
        if (state < 0.0) {
            state = 0.0;
        }
    }
    return state;
}

int main(void) {
    printf("scenario,final_state\n");
    printf("baseline,%.6f\n", simulate(10.0, 0.20, 100.0, 0.1, 300));
    printf("slow_adjustment,%.6f\n", simulate(10.0, 0.10, 100.0, 0.1, 300));
    printf("high_capacity,%.6f\n", simulate(10.0, 0.20, 140.0, 0.1, 300));
    return EXIT_SUCCESS;
}
