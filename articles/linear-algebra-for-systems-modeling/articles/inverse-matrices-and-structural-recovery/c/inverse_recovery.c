#include <stdio.h>

int main(void) {
    double a = 3, b = 1, c = 2, d = 4;
    double y1 = 7, y2 = 8;
    double det = a * d - b * c;

    if (det == 0) {
        printf("Matrix is singular; recovery is not unique.\n");
        return 1;
    }

    double x1 = (d * y1 - b * y2) / det;
    double x2 = (-c * y1 + a * y2) / det;

    printf("Recovered state: x1 = %.2f, x2 = %.2f\n", x1, x2);
    return 0;
}
