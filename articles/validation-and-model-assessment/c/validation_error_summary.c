#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const int n = 8;
    double observed[] = {70.1, 68.9, 67.4, 65.8, 64.2, 62.1, 60.4, 58.8};
    double predicted[] = {70.8, 69.7, 68.3, 66.9, 65.1, 63.8, 61.3, 59.9};

    double sum_abs = 0.0;
    double sum_sq = 0.0;
    double bias = 0.0;
    double max_abs = 0.0;

    for (int i = 0; i < n; ++i) {
        double residual = observed[i] - predicted[i];
        double abs_error = fabs(residual);
        sum_abs += abs_error;
        sum_sq += residual * residual;
        bias += residual;
        if (abs_error > max_abs) {
            max_abs = abs_error;
        }
    }

    double rmse = sqrt(sum_sq / (double)n);
    double mae = sum_abs / (double)n;
    bias = bias / (double)n;

    const char *fitness = "not_adequate_without_revision";
    if (rmse <= 1.25 && max_abs <= 2.0) {
        fitness = "adequate_for_scenario_screening";
    } else if (rmse <= 2.5) {
        fitness = "limited_use_requires_review";
    }

    printf("rmse,mae,bias,max_abs_error,fitness\n");
    printf("%.6f,%.6f,%.6f,%.6f,%s\n", rmse, mae, bias, max_abs, fitness);
    fprintf(stderr, "c validation_error_summary complete\n");
    return EXIT_SUCCESS;
}
