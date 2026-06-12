#include <stdio.h>
#include <stdlib.h>

double simulate(double initial_stock, double growth_rate, double capacity, double extraction, int steps) {
    double stock = initial_stock;
    for (int step = 0; step < steps; ++step) {
        double growth = growth_rate * stock * (1.0 - stock / capacity);
        stock = stock + growth - extraction;
        if (stock < 0.0) {
            stock = 0.0;
        }
    }
    return stock;
}

int main(void) {
    printf("scenario,final_stock\n");
    printf("baseline,%.6f\n", simulate(70.0, 0.18, 100.0, 6.0, 50));
    printf("stress,%.6f\n", simulate(70.0, 0.15, 100.0, 9.0, 50));
    printf("recovery_policy,%.6f\n", simulate(70.0, 0.18, 100.0, 5.0, 50));
    fprintf(stderr, "c workflow_resource_model complete\n");
    return EXIT_SUCCESS;
}
