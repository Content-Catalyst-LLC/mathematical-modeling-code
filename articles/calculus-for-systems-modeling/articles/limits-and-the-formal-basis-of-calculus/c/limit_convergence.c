#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double f(double x) {
    return exp(0.2 * x);
}

double exact_derivative(double x) {
    return 0.2 * exp(0.2 * x);
}

double forward_difference(double x, double h) {
    return (f(x + h) - f(x)) / h;
}

double central_difference(double x, double h) {
    return (f(x + h) - f(x - h)) / (2.0 * h);
}

double richardson(double central_h, double central_h2) {
    return (4.0 * central_h2 - central_h) / 3.0;
}

int main(void) {
    double x = 5.0;
    double exact = exact_derivative(x);
    double h_values[] = {1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125};

    printf("method,x,h,estimate,exact,absolute_error\n");

    for (int i = 0; i < 6; ++i) {
        double h = h_values[i];
        double fd = forward_difference(x, h);
        double cd = central_difference(x, h);
        double cd2 = central_difference(x, h / 2.0);
        double rich = richardson(cd, cd2);

        printf("forward_difference,%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, fd, exact, fabs(fd - exact));
        printf("central_difference,%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, cd, exact, fabs(cd - exact));
        printf("richardson_central,%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, rich, exact, fabs(rich - exact));
    }

    return EXIT_SUCCESS;
}
