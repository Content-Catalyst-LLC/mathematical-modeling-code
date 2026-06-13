#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *name;
    double baseline;
    double low;
    double high;
    const char *label;
} Parameter;

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
    Parameter params[] = {
        {"initial_stock", 80.0, 72.0, 88.0, "measurement"},
        {"growth_rate", 0.08, 0.04, 0.12, "parameter"},
        {"carrying_capacity", 120.0, 100.0, 140.0, "structural"},
        {"extraction_rate", 0.12, 0.08, 0.18, "policy"},
        {"shock_intensity", 0.03, 0.00, 0.08, "scenario"}
    };

    double baseline[5] = {80.0, 0.08, 120.0, 0.12, 0.03};
    double base_output = projection(baseline[0], baseline[1], baseline[2], baseline[3], baseline[4]);

    printf("parameter,low_output,baseline_output,high_output,range_width\n");

    for (int i = 0; i < 5; ++i) {
        double low_values[5] = {80.0, 0.08, 120.0, 0.12, 0.03};
        double high_values[5] = {80.0, 0.08, 120.0, 0.12, 0.03};
        low_values[i] = params[i].low;
        high_values[i] = params[i].high;

        double low_output = projection(low_values[0], low_values[1], low_values[2], low_values[3], low_values[4]);
        double high_output = projection(high_values[0], high_values[1], high_values[2], high_values[3], high_values[4]);
        double width = fabs(high_output - low_output);

        printf("%s,%.6f,%.6f,%.6f,%.6f\n", params[i].name, low_output, base_output, high_output, width);
    }

    fprintf(stderr, "c sensitivity_summary complete\n");
    return EXIT_SUCCESS;
}
