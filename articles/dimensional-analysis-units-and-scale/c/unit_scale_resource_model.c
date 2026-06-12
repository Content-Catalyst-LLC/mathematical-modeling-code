#include <stdio.h>
#include <stdlib.h>

static double bounded_update(double raw_next, double capacity) {
    if (raw_next < 0.0) return 0.0;
    if (raw_next > capacity) return capacity;
    return raw_next;
}

int main(void) {
    double storage = 80.0;
    const double capacity = 100.0;
    const double inflow_per_day = 8.0;
    const double demand_per_day = 6.0;
    const double loss_rate_per_day = 0.015;
    const double delta_t_days = 1.0;
    const int periods = 60;
    double total_shortage = 0.0;

    printf("period,storage_m3,inflow_volume_m3,demand_volume_m3,loss_volume_m3,raw_next_storage_m3,next_storage_m3,storage_fraction,shortage_m3\n");

    for (int period = 0; period <= periods; ++period) {
        double inflow_volume = delta_t_days * inflow_per_day;
        double demand_volume = delta_t_days * demand_per_day;
        double loss_volume = delta_t_days * loss_rate_per_day * storage;
        double raw_next = storage + inflow_volume - demand_volume - loss_volume;

        double shortage = -raw_next;
        if (shortage < 0.0) shortage = 0.0;

        double next_storage = bounded_update(raw_next, capacity);
        double storage_fraction = next_storage / capacity;

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               period, storage, inflow_volume, demand_volume, loss_volume, raw_next, next_storage, storage_fraction, shortage);

        total_shortage += shortage;
        storage = next_storage;
    }

    fprintf(stderr, "c final_storage=%.6f total_shortage=%.6f\n", storage, total_shortage);
    return EXIT_SUCCESS;
}
