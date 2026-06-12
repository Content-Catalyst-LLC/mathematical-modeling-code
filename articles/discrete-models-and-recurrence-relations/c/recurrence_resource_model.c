#include <stdio.h>
#include <stdlib.h>

static double bounded_update(double raw_next, double capacity) {
    if (raw_next < 0.0) return 0.0;
    if (raw_next > capacity) return capacity;
    return raw_next;
}

int main(void) {
    double storage = 45.0;
    double demand = 10.0;
    const double capacity = 80.0;
    const double inflow = 4.0;
    const double loss_rate = 0.020;
    const double demand_response = 0.20;
    const int periods = 60;
    double total_shortage = 0.0;
    double total_overflow = 0.0;

    printf("period,storage,demand,raw_next_storage,next_storage,shortage,overflow\n");

    for (int period = 0; period <= periods; ++period) {
        double raw_next = storage + inflow - demand - loss_rate * storage;
        double shortage = -raw_next;
        if (shortage < 0.0) shortage = 0.0;
        double overflow = raw_next - capacity;
        if (overflow < 0.0) overflow = 0.0;
        double next_storage = bounded_update(raw_next, capacity);

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               period, storage, demand, raw_next, next_storage, shortage, overflow);

        total_shortage += shortage;
        total_overflow += overflow;

        demand -= demand_response * shortage;
        if (demand < 0.0) demand = 0.0;

        storage = next_storage;
    }

    fprintf(stderr, "c final_storage=%.6f final_demand=%.6f total_shortage=%.6f total_overflow=%.6f\n",
            storage, demand, total_shortage, total_overflow);
    return EXIT_SUCCESS;
}
