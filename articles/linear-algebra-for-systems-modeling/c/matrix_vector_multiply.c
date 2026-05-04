#include <stdio.h>

int main(void) {
    double A[3][3] = {
        {0.82, 0.10, 0.08},
        {0.12, 0.76, 0.12},
        {0.06, 0.18, 0.76}
    };

    double x[3] = {0.70, 0.20, 0.10};
    double y[3] = {0.0, 0.0, 0.0};

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            y[i] += A[i][j] * x[j];
        }
    }

    printf("Transformed state: %.6f %.6f %.6f\n", y[0], y[1], y[2]);

    return 0;
}
