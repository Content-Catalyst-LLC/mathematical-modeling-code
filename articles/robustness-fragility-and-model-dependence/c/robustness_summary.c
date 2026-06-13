#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *key;
    const char *form;
    const char *scenario;
    double extraction_multiplier;
    double shock;
} Scenario;

double simulate(const char *form, double extraction_multiplier, double shock) {
    double stock = 80.0;
    const double carrying_capacity = 120.0;
    const double growth_rate = 0.08;
    const double extraction_rate = 0.12 * extraction_multiplier;
    const double fixed_loss = 5.8 * extraction_multiplier;
    const double critical_threshold = 55.0;

    for (int year = 0; year < 10; ++year) {
        if (strcmp(form, "linear_decline") == 0) {
            stock = fmax(0.0, stock - fixed_loss - shock * stock);
        } else if (strcmp(form, "logistic_recovery") == 0) {
            double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
            double extraction = extraction_rate * stock;
            stock = fmax(0.0, stock + growth - extraction - shock * stock);
        } else if (strcmp(form, "threshold_shift") == 0) {
            if (stock < critical_threshold) {
                stock = fmax(0.0, stock - 1.6 * extraction_rate * stock - shock * stock);
            } else {
                stock = fmax(0.0, stock - extraction_rate * stock - shock * stock);
            }
        }
    }

    return stock;
}

int main(void) {
    Scenario scenarios[] = {
        {"linear_baseline", "linear_decline", "baseline", 1.0, 0.00},
        {"linear_stress", "linear_decline", "stress", 1.25, 0.05},
        {"dynamic_baseline", "logistic_recovery", "baseline", 1.0, 0.00},
        {"dynamic_stress", "logistic_recovery", "stress", 1.25, 0.05},
        {"threshold_baseline", "threshold_shift", "baseline", 1.0, 0.00},
        {"threshold_stress", "threshold_shift", "stress", 1.25, 0.05}
    };

    double min_y = INFINITY;
    double max_y = -INFINITY;

    printf("key,model_form,scenario,projected_stock,below_threshold\n");

    for (int i = 0; i < 6; ++i) {
        double y = simulate(scenarios[i].form, scenarios[i].extraction_multiplier, scenarios[i].shock);
        if (y < min_y) {
            min_y = y;
        }
        if (y > max_y) {
            max_y = y;
        }
        printf("%s,%s,%s,%.6f,%s\n", scenarios[i].key, scenarios[i].form, scenarios[i].scenario, y, y < 45.0 ? "true" : "false");
    }

    fprintf(stderr, "robustness_spread=%.6f\n", max_y - min_y);
    return EXIT_SUCCESS;
}
