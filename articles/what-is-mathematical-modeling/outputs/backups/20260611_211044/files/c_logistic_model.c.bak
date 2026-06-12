#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double derivative(double x, double r, double k) {
    return r * x * (1.0 - x / k);
}

static double rk4_step(double x, double r, double k, double dt) {
    double k1 = derivative(x, r, k);
    double k2 = derivative(x + 0.5 * dt * k1, r, k);
    double k3 = derivative(x + 0.5 * dt * k2, r, k);
    double k4 = derivative(x + dt * k3, r, k);
    double next = x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4);
    return next < 0.0 ? 0.0 : next;
}

int main(void) {
    double x = 10.0;
    double r = 0.35;
    double k = 100.0;
    double dt = 0.1;
    int steps = 160;

    for (int step = 0; step <= steps; ++step) {
        if (step % 40 == 0) {
            printf("step=%d time=%.3f state=%.6f\n", step, step * dt, x);
        }
        x = rk4_step(x, r, k, dt);
    }

    printf("C RK4 final_state=%.6f\n", x);
    return EXIT_SUCCESS;
}
