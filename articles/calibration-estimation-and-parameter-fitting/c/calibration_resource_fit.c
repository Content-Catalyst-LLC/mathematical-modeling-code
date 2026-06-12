#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double score(double growth_rate, double carrying_capacity, const double *stock, const double *extraction, int n) {
    double current_stock = stock[0];
    double sse = 0.0;

    for (int i = 0; i < n; ++i) {
        double predicted = current_stock;
        if (i > 0) {
            double growth = growth_rate * current_stock * (1.0 - current_stock / carrying_capacity);
            predicted = fmax(0.0, current_stock + growth - extraction[i - 1]);
            current_stock = predicted;
        }
        double residual = stock[i] - predicted;
        sse += residual * residual;
    }

    return sse;
}

int main(void) {
    const int n = 10;
    double stock[] = {70.0,72.8,74.1,75.0,75.5,75.2,74.7,73.8,72.6,71.2};
    double extraction[] = {5.5,5.8,6.2,6.4,6.8,7.0,7.1,7.4,7.6,7.8};

    double best_sse = INFINITY;
    double best_g = 0.0;
    double best_k = 0.0;

    for (double g = 0.08; g <= 0.2600001; g += 0.01) {
        for (double k = 85.0; k <= 125.0001; k += 5.0) {
            double sse = score(g, k, stock, extraction, n);
            if (sse < best_sse) {
                best_sse = sse;
                best_g = g;
                best_k = k;
            }
        }
    }

    printf("best_growth_rate,best_carrying_capacity,sse\n");
    printf("%.6f,%.6f,%.6f\n", best_g, best_k, best_sse);
    fprintf(stderr, "c calibration_resource_fit complete\n");
    return EXIT_SUCCESS;
}
