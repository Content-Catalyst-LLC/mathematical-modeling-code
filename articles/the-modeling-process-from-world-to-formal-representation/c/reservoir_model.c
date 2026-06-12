#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double bounded_update(double storage, double inflow, double demand, double losses, double capacity) {
    double next = storage + inflow - demand - losses;
    if (next < 0.0) return 0.0;
    if (next > capacity) return capacity;
    return next;
}

int main(void) {
    double storage = 80.0;
    const double capacity = 100.0;
    const double inflow = 8.0;
    const double base_demand = 6.0;
    const double demand_growth = 0.010;
    const double loss_rate = 0.015;
    const int periods = 60;
    double total_shortage = 0.0;

    printf("period,storage,demand,losses,shortage\n");
    for (int period = 0; period <= periods; ++period) {
        double demand = base_demand * pow(1.0 + demand_growth, (double) period);
        double losses = loss_rate * storage;
        double shortage = demand + losses - (storage + inflow);
        if (shortage < 0.0) shortage = 0.0;
        printf("%d,%.6f,%.6f,%.6f,%.6f\n", period, storage, demand, losses, shortage);
        total_shortage += shortage;
        storage = bounded_update(storage, inflow, demand, losses, capacity);
    }

    fprintf(stderr, "c final_storage=%.6f total_shortage=%.6f\n", storage, total_shortage);
    return EXIT_SUCCESS;
}
