#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double piecewise_system(double x) {
    if (x < 5.0) {
        return 2.0 + 0.5 * x;
    }
    return 6.0 + 1.4 * (x - 5.0);
}

const char *classify(double level_jump, double slope_change) {
    if (level_jump > 1.0 && slope_change > 0.5) return "level_and_slope_break";
    if (level_jump > 1.0) return "possible_jump";
    if (slope_change > 0.5) return "possible_slope_break";
    return "ok";
}

int main(void) {
    const int n = 41;
    double xs[n];
    double ys[n];

    for (int i = 0; i < n; ++i) {
        xs[i] = 0.25 * i;
        ys[i] = piecewise_system(xs[i]);
    }

    printf("x,y,left_slope,right_slope,slope_change,level_jump,flag\n");

    for (int i = 0; i < n; ++i) {
        if (i == 0 || i == n - 1) {
            printf("%.6f,%.6f,,,,,ok\n", xs[i], ys[i]);
        } else {
            double left_slope = (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1]);
            double right_slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]);
            double slope_change = fabs(right_slope - left_slope);
            double level_jump = fabs(ys[i] - ys[i - 1]);
            printf("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
                xs[i], ys[i], left_slope, right_slope, slope_change, level_jump,
                classify(level_jump, slope_change));
        }
    }

    return EXIT_SUCCESS;
}
