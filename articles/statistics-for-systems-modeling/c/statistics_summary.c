#include <stdio.h>
#include <math.h>

int main(void) {
    double values[] = {18.4, 36.7, 62.1, 28.9, 64.8, 13.7, 43.5, 29.8, 79.4, 30.2};
    int n = 10;
    double sum = 0.0;

    for (int i = 0; i < n; i++) {
        sum += values[i];
    }

    double mean = sum / n;
    double ss = 0.0;

    for (int i = 0; i < n; i++) {
        ss += (values[i] - mean) * (values[i] - mean);
    }

    double variance = ss / (n - 1);
    double sd = sqrt(variance);

    printf("Mean: %.6f\n", mean);
    printf("Sample variance: %.6f\n", variance);
    printf("Sample standard deviation: %.6f\n", sd);

    return 0;
}
