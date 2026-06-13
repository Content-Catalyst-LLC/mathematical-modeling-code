#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double simulate_model(const char *form_key) {
    double stock = 80.0;
    const double carrying_capacity = 120.0;
    const double extraction_rate = 0.12;
    const double growth_rate = 0.08;
    const double fixed_loss = 5.8;
    const double critical_threshold = 55.0;

    for (int year = 0; year < 10; ++year) {
        if (strcmp(form_key, "linear_decline") == 0) {
            stock = fmax(0.0, stock - fixed_loss);
        } else if (strcmp(form_key, "proportional_decline") == 0) {
            stock = fmax(0.0, stock - extraction_rate * stock);
        } else if (strcmp(form_key, "logistic_recovery") == 0) {
            double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
            double extraction = extraction_rate * stock;
            stock = fmax(0.0, stock + growth - extraction);
        } else if (strcmp(form_key, "threshold_shift") == 0) {
            if (stock < critical_threshold) {
                stock = fmax(0.0, stock - 1.6 * extraction_rate * stock);
            } else {
                stock = fmax(0.0, stock - extraction_rate * stock);
            }
        }
    }

    return stock;
}

int main(void) {
    const char *forms[] = {
        "linear_decline",
        "proportional_decline",
        "logistic_recovery",
        "threshold_shift"
    };

    double min_y = INFINITY;
    double max_y = -INFINITY;

    printf("model_form,projected_stock,below_threshold\n");

    for (int i = 0; i < 4; ++i) {
        double y = simulate_model(forms[i]);
        if (y < min_y) {
            min_y = y;
        }
        if (y > max_y) {
            max_y = y;
        }
        printf("%s,%.6f,%s\n", forms[i], y, y < 45.0 ? "true" : "false");
    }

    fprintf(stderr, "structural_spread=%.6f\n", max_y - min_y);
    return EXIT_SUCCESS;
}
