#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double derivative(double stock, double growth_rate, double carrying_capacity, double extraction) {
    return growth_rate * stock * (1.0 - stock / carrying_capacity) - extraction;
}

double run_euler(double step_size) {
    double stock = 70.0;
    const double growth_rate = 0.18;
    const double carrying_capacity = 100.0;
    const double extraction = 6.0;
    const double horizon = 50.0;
    int steps = (int)round(horizon / step_size);

    for (int i = 0; i < steps; ++i) {
        stock = stock + step_size * derivative(stock, growth_rate, carrying_capacity, extraction);
        if (stock < 0.0) {
            stock = 0.0;
        }
    }

    return stock;
}

int main(void) {
    double step_sizes[] = {1.0, 0.5, 0.25, 0.1};
    const int count = (int)(sizeof(step_sizes) / sizeof(step_sizes[0]));
    double reference = run_euler(0.1);

    printf("step_size,final_stock,difference_from_finest\n");

    for (int i = 0; i < count; ++i) {
        double final_stock = run_euler(step_sizes[i]);
        printf("%.6f,%.6f,%.6f\n", step_sizes[i], final_stock, fabs(final_stock - reference));
    }

    fprintf(stderr, "c euler_resource_model complete\n");
    return EXIT_SUCCESS;
}
