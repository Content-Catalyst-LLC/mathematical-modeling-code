#include <stdio.h>
#include <stdlib.h>

static double derivative(double storage, double inflow_rate, double demand_rate, double loss_rate) {
    return inflow_rate - demand_rate - loss_rate * storage;
}

static double bounded_update(double raw_next, double capacity) {
    if (raw_next < 0.0) return 0.0;
    if (raw_next > capacity) return capacity;
    return raw_next;
}

int main(void) {
    double storage = 80.0;
    const double capacity = 100.0;
    const double inflow_rate = 8.0;
    const double demand_rate = 6.0;
    const double loss_rate = 0.015;
    const double dt = 0.25;
    const double horizon = 60.0;
    const int steps = (int)(horizon / dt);
    double time = 0.0;
    double total_shortage = 0.0;
    double total_overflow = 0.0;

    printf("step,time,storage,rate_of_change,raw_next_storage,next_storage,shortage,overflow\n");

    for (int step = 0; step <= steps; ++step) {
        double rate = derivative(storage, inflow_rate, demand_rate, loss_rate);
        double raw_next = storage + dt * rate;
        double shortage = -raw_next;
        if (shortage < 0.0) shortage = 0.0;
        double overflow = raw_next - capacity;
        if (overflow < 0.0) overflow = 0.0;
        double next_storage = bounded_update(raw_next, capacity);

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               step, time, storage, rate, raw_next, next_storage, shortage, overflow);

        total_shortage += shortage;
        total_overflow += overflow;
        storage = next_storage;
        time += dt;
    }

    fprintf(stderr, "c final_storage=%.6f total_shortage=%.6f total_overflow=%.6f\n",
            storage, total_shortage, total_overflow);
    return EXIT_SUCCESS;
}
