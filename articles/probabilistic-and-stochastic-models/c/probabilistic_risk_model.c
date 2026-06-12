#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static unsigned long rng_state = 123456789UL;

static double uniform01(void) {
    rng_state = (1103515245UL * rng_state + 12345UL) % 2147483648UL;
    return ((double)rng_state + 1.0) / 2147483649.0;
}

static double normal01(void) {
    double u1 = uniform01();
    double u2 = uniform01();
    if (u1 <= 0.0) u1 = 1e-12;
    return sqrt(-2.0 * log(u1)) * cos(2.0 * 3.14159265358979323846 * u2);
}

int main(void) {
    const int simulations = 1000;
    const double demand_mu = 4.50;
    const double demand_sigma = 0.25;
    const double supply_mean = 95.0;
    const double supply_sd = 8.0;
    const double reserve = 5.0;

    int shortage_events = 0;
    double total_shortage = 0.0;
    double max_shortage = 0.0;

    printf("run,demand,supply,reserve,available_supply,shortage,shortage_event\n");

    for (int run = 1; run <= simulations; ++run) {
        double demand = exp(demand_mu + demand_sigma * normal01());
        double supply = supply_mean + supply_sd * normal01();
        if (supply < 0.0) supply = 0.0;
        double available = supply + reserve;
        double shortage = demand - available;
        if (shortage < 0.0) shortage = 0.0;

        int event = shortage > 0.0 ? 1 : 0;
        shortage_events += event;
        total_shortage += shortage;
        if (shortage > max_shortage) max_shortage = shortage;

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
               run, demand, supply, reserve, available, shortage, event);
    }

    fprintf(stderr, "c shortage_probability=%.6f expected_shortage=%.6f max_shortage=%.6f\n",
            (double)shortage_events / (double)simulations,
            total_shortage / (double)simulations,
            max_shortage);
    return EXIT_SUCCESS;
}
