#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double system_response(double x) {
    return exp(0.2 * x);
}

double exact_derivative(double x) {
    return 0.2 * exp(0.2 * x);
}

double difference_quotient(double x, double h) {
    return (system_response(x + h) - system_response(x)) / h;
}

int main(void) {
    double x = 5.0;
    double exact = exact_derivative(x);
    double h_values[] = {1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001};

    printf("function_name,x,h,estimate,exact_value,absolute_error\n");

    for (int i = 0; i < 7; ++i) {
        double h = h_values[i];
        double estimate = difference_quotient(x, h);
        printf("exp(0.2x),%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, estimate, exact, fabs(estimate - exact));
    }

    return EXIT_SUCCESS;
}
