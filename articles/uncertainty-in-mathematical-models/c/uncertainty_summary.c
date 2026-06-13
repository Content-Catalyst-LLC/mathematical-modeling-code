#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double uniform_between(double low, double high) {
    return low + ((double)rand() / (double)RAND_MAX) * (high - low);
}

double projection(double initial_stock, double growth_rate, double carrying_capacity, double extraction_rate, double shock_intensity) {
    double stock = initial_stock;
    for (int year = 0; year < 10; ++year) {
        double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
        double extraction = extraction_rate * stock;
        double shock = shock_intensity * stock;
        stock = fmax(0.0, stock + growth - extraction - shock);
    }
    return stock;
}

int main(void) {
    const int n = 1000;
    int threshold_count = 0;
    double sum = 0.0;
    double min_y = INFINITY;
    double max_y = -INFINITY;

    srand(42);

    for (int i = 0; i < n; ++i) {
        double initial_stock = uniform_between(72.0, 88.0);
        double growth_rate = uniform_between(0.04, 0.12);
        double carrying_capacity = uniform_between(100.0, 140.0);
        double extraction_rate = uniform_between(0.08, 0.18);
        double shock_intensity = uniform_between(0.00, 0.08);

        double y = projection(initial_stock, growth_rate, carrying_capacity, extraction_rate, shock_intensity);
        sum += y;

        if (y < min_y) {
            min_y = y;
        }
        if (y > max_y) {
            max_y = y;
        }
        if (y < 45.0) {
            threshold_count += 1;
        }
    }

    printf("mean,threshold_probability,min,max\n");
    printf("%.6f,%.6f,%.6f,%.6f\n", sum / (double)n, threshold_count / (double)n, min_y, max_y);

    fprintf(stderr, "c uncertainty_summary complete\n");
    return EXIT_SUCCESS;
}
