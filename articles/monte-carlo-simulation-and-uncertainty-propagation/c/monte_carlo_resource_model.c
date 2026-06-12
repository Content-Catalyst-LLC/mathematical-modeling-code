#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static uint64_t rng_state = 20260612ULL;

double random_unit(void) {
    rng_state = 6364136223846793005ULL * rng_state + 1ULL;
    return (double)(rng_state >> 11) / (double)(1ULL << 53);
}

double uniform_range(double min_value, double max_value) {
    return min_value + random_unit() * (max_value - min_value);
}

double run_once(void) {
    double stock = uniform_range(65.0, 75.0);
    double growth_rate = uniform_range(0.14, 0.22);
    double extraction = uniform_range(5.0, 8.0);
    double shock_probability = uniform_range(0.02, 0.08);
    const double shock_fraction = 0.12;
    const double capacity = 100.0;

    for (int step = 0; step < 50; ++step) {
        double growth = growth_rate * stock * (1.0 - stock / capacity);
        double shock = random_unit() < shock_probability ? stock * shock_fraction : 0.0;
        stock = stock + growth - extraction - shock;
        if (stock < 0.0) {
            stock = 0.0;
        }
    }

    return stock;
}

int main(void) {
    const int replications = 1000;
    double total = 0.0;
    int depleted = 0;

    for (int i = 0; i < replications; ++i) {
        double final_stock = run_once();
        total += final_stock;
        if (final_stock <= 10.0) {
            depleted += 1;
        }
    }

    printf("replications,mean_final_stock,depletion_probability\n");
    printf("%d,%.6f,%.6f\n", replications, total / replications, (double)depleted / replications);
    fprintf(stderr, "c monte_carlo_resource_model complete\n");
    return EXIT_SUCCESS;
}
