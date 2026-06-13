#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int time;
    const char *group;
    double observed;
    double predicted;
    double threshold;
} Observation;

int main(void) {
    Observation data[] = {
        {1, "baseline", 82.0, 81.5, 70.0},
        {2, "baseline", 79.5, 80.2, 70.0},
        {3, "baseline", 77.0, 78.4, 70.0},
        {4, "baseline", 74.3, 75.6, 70.0},
        {5, "threshold", 71.5, 72.8, 70.0},
        {6, "threshold", 69.2, 71.0, 70.0},
        {7, "threshold", 67.8, 69.8, 70.0},
        {8, "stress", 65.5, 68.0, 70.0},
        {9, "stress", 63.0, 66.4, 70.0},
        {10, "stress", 61.1, 65.2, 70.0}
    };

    const int n = 10;
    double sum_abs = 0.0;
    double sum_sq = 0.0;
    double bias = 0.0;
    double max_abs = 0.0;
    int disagreements = 0;

    for (int i = 0; i < n; ++i) {
        double residual = data[i].observed - data[i].predicted;
        double abs_error = fabs(residual);
        bool observed_below = data[i].observed < data[i].threshold;
        bool predicted_below = data[i].predicted < data[i].threshold;

        sum_abs += abs_error;
        sum_sq += residual * residual;
        bias += residual;

        if (abs_error > max_abs) {
            max_abs = abs_error;
        }

        if (observed_below != predicted_below) {
            disagreements += 1;
        }
    }

    printf("mean_error,mae,rmse,max_abs_error,decision_disagreements\n");
    printf("%.6f,%.6f,%.6f,%.6f,%d\n",
           bias / (double)n,
           sum_abs / (double)n,
           sqrt(sum_sq / (double)n),
           max_abs,
           disagreements);

    fprintf(stderr, "c diagnostic_summary complete\n");
    return EXIT_SUCCESS;
}
