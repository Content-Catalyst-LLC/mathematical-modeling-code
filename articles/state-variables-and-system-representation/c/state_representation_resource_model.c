#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static double bounded_update(double raw_next, double capacity) {
    if (raw_next < 0.0) return 0.0;
    if (raw_next > capacity) return capacity;
    return raw_next;
}

int main(void) {
    const char *representation = "condition_aware";
    double storage = 45.0;
    double demand = 8.0;
    double condition = 0.85;
    const double capacity = 80.0;
    const double inflow = 4.0;
    const double loss_rate = 0.020;
    const double demand_response = 0.20;
    const double condition_decay = 0.002;
    const int periods = 60;
    double total_shortage = 0.0;

    printf("period,representation,storage,demand,condition,effective_loss_rate,raw_next_storage,next_storage,shortage\n");

    for (int period = 0; period <= periods; ++period) {
        double effective_loss_rate = loss_rate;
        if (strcmp(representation, "condition_aware") == 0) {
            effective_loss_rate = loss_rate * (1.0 + (1.0 - condition));
        }

        double losses = effective_loss_rate * storage;
        double raw_next = storage + inflow - demand - losses;
        double shortage = -raw_next;
        if (shortage < 0.0) shortage = 0.0;

        double next_storage = bounded_update(raw_next, capacity);

        printf("%d,%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               period, representation, storage, demand, condition, effective_loss_rate, raw_next, next_storage, shortage);

        total_shortage += shortage;
        demand -= demand_response * shortage;
        if (demand < 0.0) demand = 0.0;

        condition -= condition_decay * shortage;
        if (condition < 0.0) condition = 0.0;

        storage = next_storage;
    }

    fprintf(stderr, "c final_storage=%.6f final_demand=%.6f final_condition=%.6f total_shortage=%.6f\n",
            storage, demand, condition, total_shortage);
    return EXIT_SUCCESS;
}
