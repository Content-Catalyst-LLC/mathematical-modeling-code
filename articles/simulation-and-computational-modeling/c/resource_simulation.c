#include <stdio.h>
#include <stdlib.h>

int main(void) {
    double stock = 70.0;
    const double growth_rate = 0.18;
    const double capacity = 100.0;
    const double extraction = 6.0;
    const int steps = 20;

    printf("step,resource_stock\n");

    for (int step = 0; step <= steps; ++step) {
        printf("%d,%.6f\n", step, stock);
        double growth = growth_rate * stock * (1.0 - stock / capacity);
        stock = stock + growth - extraction;
        if (stock < 0.0) {
            stock = 0.0;
        }
    }

    fprintf(stderr, "c resource_simulation complete\n");
    return EXIT_SUCCESS;
}
