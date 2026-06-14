#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double linear_model(double x) {
    return 10.0 + 2.0 * x;
}

double exponential_model(double x) {
    return 10.0 * exp(0.18 * x);
}

double logistic_model(double x) {
    return 100.0 / (1.0 + exp(-0.75 * (x - 5.0)));
}

double threshold_model(double x) {
    return x < 5.0 ? 20.0 : 80.0;
}

int main(void) {
    double x = 10.0;
    printf("model,final_value\n");
    printf("linear_growth,%.6f\n", linear_model(x));
    printf("exponential_growth,%.6f\n", exponential_model(x));
    printf("logistic_growth,%.6f\n", logistic_model(x));
    printf("threshold_response,%.6f\n", threshold_model(x));
    return EXIT_SUCCESS;
}
